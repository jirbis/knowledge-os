#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def iso_from_unix(ts: Optional[float]) -> Optional[str]:
    if ts is None:
        return None
    try:
        # ChatGPT export times are typically unix seconds (float)
        dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
        return dt.isoformat()
    except Exception:
        return None


def safe_filename(s: str, maxlen: int = 120) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s\-\.\(\)\[\]]+", "", s, flags=re.UNICODE)
    s = s.replace(" ", "-").lower()
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        s = "untitled"
    return s[:maxlen]


def iter_messages(conv: Dict[str, Any]) -> List[Tuple[Optional[str], str, str]]:
    """
    Returns list of (msg_id, role, text) in approximate conversation order.
    The export uses a mapping graph; we linearize by following parent/child chain
    from the root. If that fails, we fall back to sorting by create_time when present.
    """
    mapping = conv.get("mapping") or {}
    if not mapping:
        return []

    # Build child links
    children: Dict[str, List[str]] = {}
    parents: Dict[str, Optional[str]] = {}
    for mid, node in mapping.items():
        parent = node.get("parent")
        parents[mid] = parent
        if parent:
            children.setdefault(parent, []).append(mid)

    # Find root(s): nodes without parent
    roots = [mid for mid, p in parents.items() if not p]
    root = roots[0] if roots else next(iter(mapping.keys()))

    # Walk by choosing the "main" child path: prefer single child; else sort by create_time
    def node_time(mid: str) -> float:
        node = mapping.get(mid) or {}
        msg = node.get("message") or {}
        return float(msg.get("create_time") or node.get("create_time") or 0.0)

    ordered_ids: List[str] = []
    cur = root
    visited = set()
    while cur and cur not in visited:
        visited.add(cur)
        ordered_ids.append(cur)
        ch = children.get(cur, [])
        if not ch:
            break
        if len(ch) == 1:
            cur = ch[0]
        else:
            ch_sorted = sorted(ch, key=node_time)
            cur = ch_sorted[-1]  # usually the "latest branch" is the main one

    # Extract message texts
    out: List[Tuple[Optional[str], str, str]] = []
    for mid in ordered_ids:
        node = mapping.get(mid) or {}
        msg = node.get("message")
        if not msg:
            continue
        author = (msg.get("author") or {})
        role = author.get("role") or "unknown"
        content = (msg.get("content") or {})
        ctype = content.get("content_type")

        text_parts: List[str] = []
        if ctype == "text":
            parts = content.get("parts") or []
            for p in parts:
                if isinstance(p, str):
                    text_parts.append(p)
        elif ctype in ("code", "markdown"):
            parts = content.get("parts") or []
            for p in parts:
                if isinstance(p, str):
                    text_parts.append(p)
        else:
            # ignore non-text content types for MVP
            pass

        text = "\n".join([t for t in text_parts if t.strip()]).strip()
        if text:
            out.append((mid, role, text))

    # Fallback: if empty, try sort all nodes by time
    if not out:
        items = []
        for mid, node in mapping.items():
            msg = node.get("message")
            if not msg:
                continue
            role = (msg.get("author") or {}).get("role") or "unknown"
            content = msg.get("content") or {}
            if content.get("content_type") != "text":
                continue
            parts = content.get("parts") or []
            text = "\n".join([p for p in parts if isinstance(p, str)]).strip()
            if not text:
                continue
            t = float(msg.get("create_time") or node.get("create_time") or 0.0)
            items.append((t, mid, role, text))
        items.sort(key=lambda x: x[0])
        out = [(mid, role, text) for _, mid, role, text in items]

    return out


def ensure_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA temp_store=MEMORY;")

    # Meta table
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT,
            create_time TEXT,
            update_time TEXT,
            source TEXT
        );
        """
    )

    # FTS table (content)
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts
        USING fts5(
            conversation_id UNINDEXED,
            msg_id UNINDEXED,
            role,
            content,
            tokenize = 'unicode61'
        );
        """
    )

    # Helpful index table to map msg ordering if needed later
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages_meta (
            conversation_id TEXT,
            msg_id TEXT,
            ord INTEGER,
            role TEXT,
            content TEXT,
            PRIMARY KEY (conversation_id, msg_id)
        );
        """
    )

    return conn


def upsert_conversation(conn: sqlite3.Connection, conv: Dict[str, Any], source: str) -> None:
    cid = conv.get("id") or conv.get("conversation_id")
    if not cid:
        return
    title = conv.get("title") or "Untitled"
    create_time = iso_from_unix(conv.get("create_time"))
    update_time = iso_from_unix(conv.get("update_time"))

    conn.execute(
        """
        INSERT INTO conversations (id, title, create_time, update_time, source)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            create_time=excluded.create_time,
            update_time=excluded.update_time,
            source=excluded.source;
        """,
        (cid, title, create_time, update_time, source),
    )


def refresh_messages(conn: sqlite3.Connection, cid: str, messages: List[Tuple[Optional[str], str, str]]) -> None:
    # Remove old rows for this conversation to keep index consistent
    conn.execute("DELETE FROM messages_meta WHERE conversation_id = ?;", (cid,))
    conn.execute("DELETE FROM messages_fts WHERE conversation_id = ?;", (cid,))

    for i, (mid, role, text) in enumerate(messages):
        mid = mid or f"msg_{i}"
        conn.execute(
            "INSERT OR REPLACE INTO messages_meta (conversation_id, msg_id, ord, role, content) VALUES (?, ?, ?, ?, ?);",
            (cid, mid, i, role, text),
        )
        conn.execute(
            "INSERT INTO messages_fts (conversation_id, msg_id, role, content) VALUES (?, ?, ?, ?);",
            (cid, mid, role, text),
        )


def write_normalized_md(out_dir: Path, conv: Dict[str, Any], messages: List[Tuple[Optional[str], str, str]]) -> Path:
    cid = conv.get("id") or "unknown"
    title = (conv.get("title") or "Untitled").strip()
    slug = safe_filename(title)
    fname = f"{slug}__{cid}.md"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / fname

    created = iso_from_unix(conv.get("create_time")) or ""
    updated = iso_from_unix(conv.get("update_time")) or ""

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("```yaml")
    lines.append(f"conversation_id: {cid}")
    if created:
        lines.append(f"created_at: {created}")
    if updated:
        lines.append(f"updated_at: {updated}")
    lines.append("source: chatgpt_export")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    for _, role, text in messages:
        role_label = role.upper()
        lines.append(f"## {role_label}")
        lines.append(text)
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description="Ingest ChatGPT export conversations.json into normalized markdown + SQLite FTS5 index.")
    ap.add_argument("--input", required=True, help="Path to conversations.json (from ChatGPT export)")
    ap.add_argument("--db", default="index/chats.sqlite", help="SQLite db path")
    ap.add_argument("--normalized-dir", default="archive/normalized", help="Where to write normalized markdown")
    ap.add_argument("--source", default="chatgpt_export", help="Source label")
    args = ap.parse_args()

    input_path = Path(args.input)
    db_path = Path(args.db)
    normalized_dir = Path(args.normalized_dir)

    data = json.loads(input_path.read_text(encoding="utf-8"))

    # Export formats vary: sometimes it's a dict with "conversations", sometimes list
    if isinstance(data, dict) and "conversations" in data:
        conversations = data["conversations"]
    elif isinstance(data, list):
        conversations = data
    else:
        raise SystemExit("Unsupported export format: expected list or dict with 'conversations'")

    conn = ensure_db(db_path)
    processed = 0

    for conv in conversations:
        cid = conv.get("id") or conv.get("conversation_id")
        if not cid:
            continue

        msgs = iter_messages(conv)
        upsert_conversation(conn, conv, args.source)
        refresh_messages(conn, cid, msgs)
        write_normalized_md(normalized_dir, conv, msgs)
        processed += 1

        if processed % 50 == 0:
            conn.commit()

    conn.commit()
    conn.close()

    print(f"OK: processed {processed} conversations")
    print(f"DB: {db_path}")
    print(f"Normalized: {normalized_dir}")


if __name__ == "__main__":
    main()

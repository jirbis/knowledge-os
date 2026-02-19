#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def iso_from_unix(ts) -> Optional[str]:
    """Convert a Unix timestamp (int, float, or string) to ISO 8601 UTC."""
    if ts is None:
        return None
    try:
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


def extract_text(msg: Dict[str, Any]) -> str:
    """
    Extract plain text from a Telegram message.

    The 'text' field can be:
      - a plain string: "Hello world"
      - a list of entity objects:  [{"type": "plain", "text": "Hello "}, ...]
    Entity types we render: plain, bold, italic, code, pre, text_link, mention, hashtag, etc.
    Everything becomes its text component; formatting is intentionally dropped.
    """
    raw = msg.get("text")
    if raw is None:
        return ""
    if isinstance(raw, str):
        return raw.strip()
    if isinstance(raw, list):
        parts = []
        for entity in raw:
            if isinstance(entity, str):
                parts.append(entity)
            elif isinstance(entity, dict):
                parts.append(entity.get("text", ""))
        return "".join(parts).strip()
    return ""


# ---------------------------------------------------------------------------
# Message iteration
# ---------------------------------------------------------------------------

def iter_telegram_messages(chat: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    """
    Returns list of (msg_id, role, text) for a single Telegram chat.

    Filters:
    - Skip service messages (type != "message")
    - Skip messages with no extractable text
    The 'role' field stores the sender's display name.
    """
    out: List[Tuple[str, str, str]] = []
    for msg in chat.get("messages") or []:
        if msg.get("type") != "message":
            continue  # service events (pin, call, join, etc.)

        text = extract_text(msg)
        if not text:
            continue  # media-only messages (photos, stickers, videos, etc.)

        msg_id = str(msg.get("id", ""))
        if not msg_id:
            continue

        # Use sender display name as role; fall back to from_id if unnamed
        role = msg.get("from") or msg.get("from_id") or "unknown"
        out.append((msg_id, role, text))

    return out


# ---------------------------------------------------------------------------
# Change-detection helper
# ---------------------------------------------------------------------------

def load_existing_update_times(db_path: Path) -> Dict[str, Optional[str]]:
    """Return {conversation_id: update_time} for all rows already in the DB."""
    if not db_path.exists():
        return {}
    conn = sqlite3.connect(str(db_path))
    rows = conn.execute("SELECT id, update_time FROM conversations").fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def ensure_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA temp_store=MEMORY;")

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

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS imported_images (
            filename TEXT PRIMARY KEY,
            source_path TEXT,
            dest_path TEXT,
            imported_at TEXT
        );
        """
    )

    return conn


def upsert_conversation(
    conn: sqlite3.Connection,
    cid: str,
    title: str,
    create_time: Optional[str],
    update_time: Optional[str],
    source: str,
) -> None:
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


def refresh_messages(
    conn: sqlite3.Connection,
    cid: str,
    messages: List[Tuple[str, str, str]],
) -> None:
    conn.execute("DELETE FROM messages_meta WHERE conversation_id = ?;", (cid,))
    conn.execute("DELETE FROM messages_fts WHERE conversation_id = ?;", (cid,))
    for i, (mid, role, text) in enumerate(messages):
        conn.execute(
            "INSERT OR REPLACE INTO messages_meta "
            "(conversation_id, msg_id, ord, role, content) VALUES (?, ?, ?, ?, ?);",
            (cid, mid, i, role, text),
        )
        conn.execute(
            "INSERT INTO messages_fts (conversation_id, msg_id, role, content) VALUES (?, ?, ?, ?);",
            (cid, mid, role, text),
        )


# ---------------------------------------------------------------------------
# Normalized markdown output
# ---------------------------------------------------------------------------

def write_normalized_md(
    out_dir: Path,
    cid: str,
    title: str,
    create_time: Optional[str],
    update_time: Optional[str],
    messages: List[Tuple[str, str, str]],
) -> Path:
    slug = safe_filename(title)
    fname = f"{slug}__{cid}.md"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / fname

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("```yaml")
    lines.append(f"conversation_id: {cid}")
    if create_time:
        lines.append(f"created_at: {create_time}")
    if update_time:
        lines.append(f"updated_at: {update_time}")
    lines.append("source: telegram_export")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    for _, role, text in messages:
        lines.append(f"## {role}")
        lines.append(text)
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Image sync
# ---------------------------------------------------------------------------

def sync_images(images_dir: Path, dest_dir: Path, conn: sqlite3.Connection) -> Tuple[int, int]:
    """Copy new image files from images_dir to dest_dir. Returns (copied, skipped)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    existing = {row[0] for row in conn.execute("SELECT filename FROM imported_images")}
    copied, skipped = 0, 0
    for img_path in sorted(images_dir.iterdir()):
        if not img_path.is_file():
            continue
        if img_path.name in existing:
            skipped += 1
            continue
        dest = dest_dir / img_path.name
        dest.write_bytes(img_path.read_bytes())
        now = datetime.now(tz=timezone.utc).isoformat()
        conn.execute(
            "INSERT OR IGNORE INTO imported_images (filename, source_path, dest_path, imported_at) "
            "VALUES (?, ?, ?, ?)",
            (img_path.name, str(img_path), str(dest), now),
        )
        copied += 1
    return copied, skipped


# ---------------------------------------------------------------------------
# Export format detection
# ---------------------------------------------------------------------------

def collect_chats(data: Any) -> List[Dict[str, Any]]:
    """
    Telegram Desktop exports two formats:

    Single-chat export (most common):
        {"name": "...", "type": "personal_chat", "id": 123, "messages": [...]}

    All-chats export (via "Export all data"):
        {"about": "...", "chats": {"about": "...", "list": [{...}, {...}]}}

    Returns a flat list of chat dicts, each with "id", "name"/"type", and "messages".
    """
    if isinstance(data, list):
        # Rare: array of chat objects
        return data

    if isinstance(data, dict):
        # All-chats format
        if "chats" in data:
            chats_block = data["chats"]
            if isinstance(chats_block, dict):
                return chats_block.get("list") or []
            if isinstance(chats_block, list):
                return chats_block

        # Single-chat format
        if "messages" in data:
            return [data]

    raise SystemExit(
        "Unsupported Telegram export format. "
        "Expected a single-chat object (with 'messages') or an all-chats export (with 'chats.list')."
    )


# ---------------------------------------------------------------------------
# Timestamp helpers for a chat
# ---------------------------------------------------------------------------

def chat_timestamps(chat: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """
    Derive (create_time, update_time) for a chat from its messages.
    create_time = first message timestamp
    update_time = last message timestamp
    Falls back to None if no messages or timestamps are available.
    """
    messages = [m for m in (chat.get("messages") or []) if m.get("type") == "message"]
    if not messages:
        return None, None

    def msg_ts(m: Dict[str, Any]) -> Optional[float]:
        ts = m.get("date_unixtime")
        if ts is not None:
            try:
                return float(ts)
            except Exception:
                pass
        # Fallback: parse ISO date string
        date_str = m.get("date")
        if date_str:
            try:
                dt = datetime.fromisoformat(date_str)
                return dt.timestamp()
            except Exception:
                pass
        return None

    timestamps = [t for t in (msg_ts(m) for m in messages) if t is not None]
    if not timestamps:
        return None, None

    return iso_from_unix(min(timestamps)), iso_from_unix(max(timestamps))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Ingest Telegram JSON export into normalized markdown + SQLite FTS5 index."
    )
    ap.add_argument("--input", required=True,
                    help="Path to Telegram result.json export file")
    ap.add_argument("--db", default="index/chats.sqlite",
                    help="SQLite db path (shared with ChatGPT ingest)")
    ap.add_argument("--normalized-dir", default="import/normalized",
                    help="Where to write normalized markdown")
    ap.add_argument("--source", default="telegram_export",
                    help="Source label stored in DB")
    ap.add_argument("--force", action="store_true",
                    help="Reprocess all chats even if update_time is unchanged")
    ap.add_argument("--images-dir", default=None,
                    help="Path to media/image directory from Telegram export (e.g. photos/)")
    ap.add_argument("--images-dest", default="import/images",
                    help="Destination directory for copied images (default: import/images)")
    args = ap.parse_args()

    input_path = Path(args.input)
    db_path = Path(args.db)
    normalized_dir = Path(args.normalized_dir)

    data = json.loads(input_path.read_text(encoding="utf-8"))
    chats = collect_chats(data)

    conn = ensure_db(db_path)
    existing_times: Dict[str, Optional[str]] = {} if args.force else load_existing_update_times(db_path)

    stats = {"new": 0, "updated": 0, "skipped": 0}
    commit_counter = 0

    for chat in chats:
        raw_id = chat.get("id")
        if raw_id is None:
            continue

        # Prefix with "telegram_" to avoid collisions with ChatGPT UUIDs
        cid = f"telegram_{raw_id}"
        title = (chat.get("name") or f"Telegram chat {raw_id}").strip()

        create_time, update_time = chat_timestamps(chat)

        # Incremental check
        if not args.force and cid in existing_times:
            if existing_times[cid] == update_time:
                stats["skipped"] += 1
                continue
            stats["updated"] += 1
        else:
            stats["new"] += 1

        msgs = iter_telegram_messages(chat)
        upsert_conversation(conn, cid, title, create_time, update_time, args.source)
        refresh_messages(conn, cid, msgs)
        write_normalized_md(normalized_dir, cid, title, create_time, update_time, msgs)
        commit_counter += 1

        if commit_counter % 50 == 0:
            conn.commit()

    conn.commit()

    # Sync images if requested
    img_copied, img_skipped = 0, 0
    if args.images_dir:
        images_dir = Path(args.images_dir)
        if images_dir.is_dir():
            img_copied, img_skipped = sync_images(images_dir, Path(args.images_dest), conn)
            conn.commit()
        else:
            print(f"Warning: --images-dir '{images_dir}' is not a directory, skipping image sync")

    conn.close()

    total = stats["new"] + stats["updated"] + stats["skipped"]
    print(f"Chats: {stats['new']} new, {stats['updated']} updated, {stats['skipped']} skipped (of {total} total)")
    if args.images_dir:
        print(f"Images: {img_copied} copied, {img_skipped} skipped")
    print(f"DB: {db_path}")
    print(f"Normalized: {normalized_dir}")


if __name__ == "__main__":
    main()

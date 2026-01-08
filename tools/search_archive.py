#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
from pathlib import Path
from typing import List, Tuple


def connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def search(conn: sqlite3.Connection, q: str, limit: int) -> List[sqlite3.Row]:
    # Use bm25 for ranking (lower is better)
    sql = """
    SELECT
      m.conversation_id,
      c.title,
      c.create_time,
      c.update_time,
      m.role,
      snippet(messages_fts, 3, '[', ']', '…', 20) AS snippet,
      bm25(messages_fts) AS rank
    FROM messages_fts m
    JOIN conversations c ON c.id = m.conversation_id
    WHERE messages_fts MATCH ?
    ORDER BY rank
    LIMIT ?;
    """
    return list(conn.execute(sql, (q, limit)))


def main() -> None:
    ap = argparse.ArgumentParser(description="Search ChatGPT archive index (SQLite FTS5).")
    ap.add_argument("--db", default="index/chats.sqlite", help="SQLite db path")
    ap.add_argument("--q", required=True, help="FTS query. Examples: jira, \"executable protocols\", jira NEAR/5 confluence")
    ap.add_argument("--limit", type=int, default=20, help="Max results")
    args = ap.parse_args()

    conn = connect(Path(args.db))
    rows = search(conn, args.q, args.limit)

    for i, r in enumerate(rows, 1):
        print(f"\n[{i}] {r['title']}")
        print(f"    conversation_id: {r['conversation_id']}")
        if r["create_time"] or r["update_time"]:
            print(f"    created: {r['create_time']}  updated: {r['update_time']}")
        print(f"    role: {r['role']}")
        print(f"    snippet: {r['snippet']}")
    if not rows:
        print("No results.")
    conn.close()


if __name__ == "__main__":
    main()

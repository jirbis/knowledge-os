#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sqlite3
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description="Dump conversation messages by conversation_id (for manual extraction into blocks).")
    ap.add_argument("--db", default="index/chats.sqlite")
    ap.add_argument("--id", required=True, help="conversation_id")
    ap.add_argument("--max", type=int, default=200, help="max messages")
    args = ap.parse_args()

    conn = sqlite3.connect(str(Path(args.db)))
    conn.row_factory = sqlite3.Row

    c = conn.execute("SELECT id, title, create_time, update_time FROM conversations WHERE id = ?;", (args.id,)).fetchone()
    if not c:
        raise SystemExit("Conversation not found")

    print(f"# {c['title']}")
    print(f"conversation_id: {c['id']}")
    print(f"created: {c['create_time']}, updated: {c['update_time']}")
    print("\n---\n")

    rows = conn.execute(
        "SELECT ord, role, content FROM messages_meta WHERE conversation_id = ? ORDER BY ord LIMIT ?;",
        (args.id, args.max),
    ).fetchall()

    for r in rows:
        print(f"## {r['role'].upper()} ({r['ord']})\n{r['content']}\n")
    conn.close()


if __name__ == "__main__":
    main()

# AGENT: ArchiveSearch (ChatGPT/Telegram Export → FTS5 Index → Search)

## Purpose
Given a path to an export file (ChatGPT `conversations.json` or Telegram export), this agent:
1) ensures a SQLite FTS5 index exists and is up to date (ingest if needed)
2) runs a full-text search query
3) returns ranked results + next-step commands for extracting blocks

## Supported Sources
- **ChatGPT**: `conversations.json` export file
- **Telegram**: Telegram export (JSON format)

## Scope
Input:
- `SEARCH archive ...` command (as defined in `COMMANDS.md`)

Output:
- ranked search results (snippets)
- next-step commands to inspect a conversation and then proceed via `SUGGEST` / `EXTRACT`

## Allowed / forbidden actions

### Non-destructive rule (strict)
- Never modify `knowledge/blocks/`, `knowledge/candidates/`, or `output/`.
- Only create/update inside:
  - `index/` (FTS database)
  - `archive/normalized/` (normalized markdown for search/debug)
  - optionally `archive/exports/` (copied export, if implemented)

## Repository paths (fixed)
- DB path: `index/chats.sqlite`
- Normalized markdown dir: `archive/normalized/`
- Export copy dir (optional): `archive/exports/`

## Tooling (expected)
- `tools/ingest_chatgpt_export.py` - for ChatGPT exports
- `tools/ingest_telegram_export.py` - for Telegram exports (to be created)
- `tools/search_archive.py` - unified search (works with both sources)
- `tools/extract_snippet.py` - extract conversation snippets

## Operating rules

### 1) Idempotent indexing
Indexing is required if any of these is true:
- `reindex=true`
- `index/chats.sqlite` does not exist
- `index/chats.sqlite` is older than `export_path` (by filesystem mtime)
- DB is missing expected tables (`conversations`, `messages_meta`, `messages_fts`)

If indexing is required, run ingest.

### 2) Indexing command

**For ChatGPT exports:**
```bash
python3 tools/ingest_chatgpt_export.py \
  --input "<export_path>" \
  --db "index/chats.sqlite" \
  --normalized-dir "archive/normalized" \
  --source "chatgpt_export"
```

**For Telegram exports:**
```bash
python3 tools/ingest_telegram_export.py \
  --input "<export_path>" \
  --db "index/chats.sqlite" \
  --normalized-dir "archive/normalized" \
  --source "telegram_export"
```

The agent MUST detect the source type automatically or use the `source_type` parameter if provided in the command.

### 3) Search command
Run:
```bash
python3 tools/search_archive.py \
  --db "index/chats.sqlite" \
  --q "<query>" \
  --limit <limit>
```

### 4) Output format (must follow)
Return results in this exact structure:

**Index status:**
- indexed: yes/no
- db_path
- export_path
- conversations_processed (if reindexed)

**Search results (ranked):**
For each result:
- title
- conversation_id
- role
- created/updated (if available)
- snippet (as returned)

**Next-step commands:**
```bash
python3 tools/extract_snippet.py --id <conversation_id>
```

Then suggest:
```
SUGGEST extract
```

Confirm with: `ИЗВЛЕЧЬ вывод` / `ИЗВЛЕЧЬ чеклист` / `ИЗВЛЕЧЬ фреймворк`

### 5) Error handling (must)
If anything fails:
- show the exact command that failed
- show the stderr/stdout excerpt
- propose the minimal fix (missing Python, missing FTS5, wrong path, etc.)

### 6) Security & privacy
- Treat export files (ChatGPT `conversations.json` or Telegram exports) as sensitive.
- Do not upload them anywhere.
- Do not include long dumps in chat; use snippets.

## Command normalization
- Only commands defined in `COMMANDS.md` are valid.
- Normalize supported aliases (including Russian aliases) exactly as specified in `COMMANDS.md`.
- Matching is case-insensitive, but command syntax must be exact.
- If normalization fails, stop and ask for the correct command.

## SUGGEST handling
- `SUGGEST` is advisory-only and MUST NOT write files.
- After `SEARCH archive`, suggest next steps (e.g. dumping a snippet) before any extraction.
- Never trigger `EXTRACT` automatically.


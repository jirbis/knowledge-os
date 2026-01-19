# SEARCH — archive search (ChatGPT/Telegram) (read-only)

## Purpose

Given a path to an export file (ChatGPT `conversations.json` or Telegram export), this command:
1) ensures a SQLite FTS5 index exists and is up to date (ingest if needed)
2) runs a full-text search query
3) returns ranked results + next-step commands for extracting blocks

Search through exported ChatGPT or Telegram chats  
with automatic FTS5 indexing if needed.

SEARCH **never creates knowledge blocks**.  
It only finds raw material for subsequent `SUGGEST` / `EXTRACT`.

## Supported Sources

- **ChatGPT**: `conversations.json` export file
- **Telegram**: Telegram export (JSON format)

## Scope

**Input:**
- `SEARCH archive ...` command

**Output:**
- ranked search results (snippets)
- next-step commands to inspect a conversation and then proceed via `SUGGEST` / `EXTRACT`

## Canonical command (internal)

```
SEARCH archive
```

## Supported parameters

```
export_path=<path/to/export>              # required on first run
query="<fts query>"                       # required
source_type=<chatgpt|telegram>            # optional, auto-detect if not specified
limit=<int>                               # optional, default 20
reindex=<true|false>                      # optional, default false
```

**Examples:**

ChatGPT:
```
SEARCH archive export_path=$GIT_ROOT/conversations.json query="jira NEAR/5 workflow" limit=20
```

Telegram:
```
SEARCH archive export_path=telegram_export.json source_type=telegram query="project discussion" limit=20
```

## Russian aliases

- ПОИСК архив → SEARCH archive
- НАЙТИ в архиве → SEARCH archive

## Allowed actions

- Creation / update:
  - `index/chats.sqlite`
  - `import/normalized/*`
- Reading export files (ChatGPT `conversations.json` or Telegram export)

## Forbidden actions

- ❌ Modify `blocks/`
- ❌ Trigger EXTRACT automatically
- ❌ Save search results
- ❌ Never modify `blocks/` or `export/`

## Tooling (expected)

- `tools/ingest_chatgpt_export.py` - for ChatGPT exports
- `tools/ingest_telegram_export.py` - for Telegram exports (to be created)
- `tools/search_archive.py` - unified search (works with both sources)
- `tools/extract_snippet.py` - extract conversation snippets

## Command behavior

1. Checks for index:
   - `index/chats.sqlite`
2. If index is missing or outdated:
   - automatically runs ingest (FTS5)
3. Executes FTS5 search
4. Returns:
   - sorted results
   - conversation_id
   - short snippet
   - next-step hints

## Operating rules

### 1) Idempotent indexing

See `.cursor/rules.md` §8 for idempotent indexing rules.

### 2) Indexing command

**For ChatGPT exports:**
```bash
python3 tools/ingest_chatgpt_export.py \
  --input "<export_path>" \
  --db "index/chats.sqlite" \
  --normalized-dir "import/normalized" \
  --source "chatgpt_export"
```

**For Telegram exports:**
```bash
python3 tools/ingest_telegram_export.py \
  --input "<export_path>" \
  --db "index/chats.sqlite" \
  --normalized-dir "import/normalized" \
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

### 5) Error handling (must)

If anything fails:
- show the exact command that failed
- show the stderr/stdout excerpt
- propose the minimal fix (missing Python, missing FTS5, wrong path, etc.)

### 6) Security & privacy

- Treat export files (ChatGPT `conversations.json` or Telegram exports) as sensitive.
- Do not upload them anywhere.
- Do not include long dumps in chat; use snippets.

## Typical workflow

```
SEARCH archive ...
↓
(view results)
↓
python3 tools/extract_snippet.py --id <conversation_id>
↓
SUGGEST extract
↓
ИЗВЛЕЧЬ вывод / чеклист / фреймворк
```

## Query hints (FTS5)

- Exact phrase:
  `"executable protocols"`
- Logic:
  `jira OR confluence`
- Proximity:
  `jira NEAR/5 workflow`
- Exclusion:
  `jira NOT datacenter`

## Non-destructive Rule (Strict)

- Never modify `blocks/` or `export/`.
- Only create/update inside:
  - `index/` (FTS database)
  - `import/normalized/` (normalized markdown for search/debug)
  - optionally `import/` (copied export, if implemented)

## Repository Paths (Fixed)

- DB path: `index/chats.sqlite`
- Normalized markdown dir: `import/normalized/`
- Import copy dir (optional): `import/`

## Guarantees

- SEARCH is safe
- SEARCH is reversible
- SEARCH does not pollute knowledge base

When in doubt — use SEARCH, not EXTRACT.

See `.cursor/rules.md` for:
- General principles (§1)
- Command normalization (§2)
- Allowed write locations (§3)
- Global safety rules (§10-12)
- Global rules (§15)

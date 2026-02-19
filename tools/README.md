# Knowledge OS Tools

Tools for managing Knowledge OS repositories, semantic search, and enforcing boundaries.

---

## Semantic Search (New)

### `embed_blocks.py`

Generate embeddings for all knowledge-os blocks for semantic search.

**Usage:**
```bash
python3 tools/embed_blocks.py [--blocks-dir ./blocks] [--output ./index/embeddings.sqlite] [--model openai]
```

**Options:**
- `--blocks-dir` — Path to blocks directory (default: ./blocks)
- `--output` — Output SQLite database (default: ./index/embeddings.sqlite)
- `--model` — Embedding model: `openai` or `local` (default: openai)
- `--chunk-size` — Chunk size in tokens (default: 512)
- `--overlap` — Chunk overlap in tokens (default: 64)
- `--force` — Force re-embedding of all blocks

**Requirements:**
- For OpenAI: `pip install openai` + `OPENAI_API_KEY` env var
- For local: `pip install sentence-transformers`

---

### `semantic_search.py`

Query embeddings for semantic search over knowledge-os blocks.

**Usage:**
```bash
python3 tools/semantic_search.py --query "marketing funnel" [--limit 10] [--type frameworks]
```

**Options:**
- `--query, -q` — Search query (required)
- `--db` — Embeddings database (default: ./index/embeddings.sqlite)
- `--limit, -n` — Maximum results (default: 10)
- `--type, -t` — Filter by block type (frameworks, checklists, plans, etc.)
- `--threshold` — Minimum similarity score 0-1 (default: 0.3)
- `--output, -o` — Output format: text, json, or markdown (default: text)
- `--fallback` — FTS5 database path for fallback search

**Examples:**
```bash
# Basic search
python3 tools/semantic_search.py -q "marketing funnel"

# Filter by type, JSON output
python3 tools/semantic_search.py -q "lead scoring" -t frameworks -o json

# With FTS5 fallback
python3 tools/semantic_search.py -q "workflow" --fallback ./index/chats.sqlite
```

---

### `read_block.py`

Read a single block with metadata from knowledge-os.

**Usage:**
```bash
python3 tools/read_block.py <block_id> [--output json|yaml|markdown]
python3 tools/read_block.py --list [--type <type>]
```

**Options:**
- `block_id` — Block ID (e.g., frameworks.marketing-funnel-project-framework)
- `--path, -p` — Read by file path instead of block ID
- `--output, -o` — Output format: json, yaml, or markdown (default: markdown)
- `--list, -l` — List all available blocks
- `--type, -t` — Filter by type when listing

**Examples:**
```bash
# Read block by ID
python3 tools/read_block.py frameworks.marketing-funnel-project-framework

# List all blocks
python3 tools/read_block.py --list

# List only checklists
python3 tools/read_block.py --list --type checklists
```

---

### `assemble_blocks.py`

Combine multiple blocks into a single output document.

**Usage:**
```bash
python3 tools/assemble_blocks.py --blocks <block_ids...> --output <output.md>
python3 tools/assemble_blocks.py --query "marketing funnel" --output <output.md>
```

**Options:**
- `--blocks, -b` — Block IDs to assemble (space-separated)
- `--query, -q` — Search query to find blocks to assemble
- `--output, -o` — Output file path (required)
- `--format, -f` — Output format: markdown, json (default: markdown)
- `--title` — Title for assembled document
- `--limit, -n` — Max blocks when using query (default: 5)

**Examples:**
```bash
# Assemble specific blocks
python3 tools/assemble_blocks.py -b frameworks.marketing-funnel-project-framework checklists.kanban-for-rollout -o ./export/funnel-guide.md

# Assemble by search query
python3 tools/assemble_blocks.py -q "marketing automation" -o ./export/marketing-automation.md --title "Marketing Automation Guide"
```

---

## Repository Management

### `init_repository.py`

Initialize repository structures for different repository types.

**Usage:**
```bash
python3 tools/init_repository.py <type> [path] [options]
```

**Usage:**
```bash
# Initialize monorepo in current directory
python3 tools/init_repository.py .

# Initialize monorepo in specific path
python3 tools/init_repository.py /path/to/repo
```

---

## Validation

### `validate_repository_boundaries.py`

Enforce repository boundaries and validate read-only access patterns.

**Usage:**
```bash
python3 tools/validate_repository_boundaries.py [options]
```

**Options:**
- `--config <path>` — Path to config.yaml (default: ./config.yaml)
- `--check-path <path>` — Check if a specific path is protected

**Examples:**
```bash
# Check if a path is protected
python3 tools/validate_repository_boundaries.py --check-path ./knowledge/blocks

# Full validation
python3 tools/validate_repository_boundaries.py
```

**Exit codes:**
- `0` — All validations passed
- `1` — Validation failed

**Integration with agents:**
Assembler agent should call this script before write operations:
```bash
python3 tools/validate_repository_boundaries.py --check-path <target-path>
```

---

## Archive & Search (FTS5)

### `ingest_chatgpt_export.py`

Ingest ChatGPT export into FTS5 index.

### `ingest_telegram_export.py`

Ingest Telegram JSON export (`result.json`) into the shared FTS5 index. Supports single-chat
and all-chats exports, incremental re-ingestion, and optional media file sync.

```bash
# Single-chat or all-chats export
python3 tools/ingest_telegram_export.py \
  --input /path/to/result.json \
  --db index/chats.sqlite \
  --normalized-dir import/normalized

# With photos directory
python3 tools/ingest_telegram_export.py \
  --input /path/to/result.json \
  --images-dir /path/to/photos \
  --images-dest import/images

# Force full reprocess
python3 tools/ingest_telegram_export.py \
  --input /path/to/result.json \
  --force
```

**Flags:** `--input`, `--db`, `--normalized-dir`, `--source`, `--force`, `--images-dir`, `--images-dest`

Conversation IDs are prefixed with `telegram_` (e.g. `telegram_12345`) to avoid collisions with
ChatGPT UUIDs in the shared database. Incremental detection uses the last message timestamp as
`update_time`.

### `search_archive.py`

Search indexed conversations using FTS5.

### `extract_snippet.py`

Extract conversation snippet by ID.

---

## Related Documentation

- **Configuration:** `config.yaml`
- **Getting Started:** `docs/Getting-Started.md`

# Knowledge OS Tools

Tools for managing Knowledge OS repositories and enforcing boundaries.

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

## Archive & Search

### `ingest_chatgpt_export.py`

Ingest ChatGPT export into FTS5 index.

### `ingest_telegram_export.py`

(To be created) Ingest Telegram export into FTS5 index.

### `search_archive.py`

Search indexed conversations.

### `extract_snippet.py`

Extract conversation snippet by ID.

---

## Related Documentation

- **Configuration:** `config.yaml`
- **Getting Started:** `docs/Getting-Started.md`

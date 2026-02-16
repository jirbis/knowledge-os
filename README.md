# Knowledge-OS

A constitutional agent architecture for systematic knowledge extraction, organization, and assembly.

Knowledge-OS turns conversations and unstructured content into reusable **knowledge blocks** — atomic, typed, and searchable — then assembles them into structured output documents.

---

## How It Works

```
Conversations / Exports
        │
        ▼
   [ EXTRACT ]  →  blocks/        (one block = one idea)
        │
        ▼
   [ SEARCH ]   →  index/         (semantic + full-text search)
        │
        ▼
   [ ASSEMBLE ] →  export/        (assembled documents)
```

**Blocks** are the fundamental unit. Each block contains one idea with YAML frontmatter (type, themes, confidence, tags). Blocks are never deleted — only deprecated.

## Block Types

| Type | Purpose |
|------|---------|
| `framework` | Reusable structure or model |
| `checklist` | Actionable steps |
| `conclusion` | Clear insight or decision |
| `narrative` | Story, vignette, or example |
| `plan` | Action plan |
| `pattern` | Repeatable pattern |

---

## Commands

All operations go through explicit commands defined in `.cursor/commands/`:

| Command | Description | Writes To |
|---------|-------------|-----------|
| `EXTRACT` | Extract knowledge blocks from conversations | `./blocks/` |
| `ASSEMBLE` | Assemble content from existing blocks | `./export/` |
| `SEARCH` | Import and search ChatGPT/Telegram archives | `./index/` |
| `ORGANIZE` | Suggest organization improvements | _(read-only)_ |
| `SUGGEST` | Suggest actions without executing | _(read-only)_ |
| `STATUS` | Candidate state management | — |
| `HELP` | Command reference | — |

---

## Repository Structure

```
knowledge-os/
├── blocks/                # Knowledge blocks (source of truth)
│   ├── frameworks/
│   ├── checklists/
│   ├── conclusions/
│   ├── narratives/
│   ├── plans/
│   └── patterns/
├── export/                # Assembled output documents
├── import/normalized/     # Normalized markdown for indexing
├── index/                 # Search databases (embeddings + FTS5)
├── tools/                 # Python utilities
├── .cursor/
│   ├── rules.md           # Canonical rules
│   └── commands/          # Command definitions
└── config.yaml            # Pipeline configuration
```

---

## Tools

### Semantic Search

```bash
# Generate embeddings for all blocks
python3 tools/embed_blocks.py

# Search blocks by meaning
python3 tools/semantic_search.py -q "marketing funnel" -t frameworks

# Read a single block with metadata
python3 tools/read_block.py frameworks.my-block-id

# Assemble blocks into a document
python3 tools/assemble_blocks.py -b block.id-1 block.id-2 -o ./export/output.md
```

### Archive & Search

```bash
# Ingest a ChatGPT export
python3 tools/ingest_chatgpt_export.py <export.zip>

# Full-text search over archived conversations
python3 tools/search_archive.py "query"

# Extract a conversation snippet
python3 tools/extract_snippet.py <conversation_id>
```

### Validation

```bash
# Check if a path is protected
python3 tools/validate_repository_boundaries.py --check-path ./blocks

# Run full boundary validation
python3 tools/validate_repository_boundaries.py
```

### Dependencies

- Python 3.8+
- For OpenAI embeddings: `pip install openai` + `OPENAI_API_KEY` env var
- For local embeddings: `pip install sentence-transformers`
- For config parsing: `pip install pyyaml`

---

## Constitutional Rules

Knowledge-OS enforces strict rules to preserve meaning integrity:

1. **Command authority** — only commands defined in `.cursor/commands/` are valid
2. **Write boundaries** — writes only to `./blocks/`, `./export/`, `./import/normalized/`, `./index/`
3. **One block, one idea** — blocks must be reusable without context
4. **No invention** — agents extract and assemble, never create new claims
5. **No drift** — assembled content must match source blocks exactly
6. **Safety & reversibility** — all operations reversible via git
7. **One rule above all** — _"If it is not in a block, it does not exist"_

See `.cursor/rules.md` for the full canonical ruleset.

---

## Architecture

Knowledge-OS is built on the **Constitutional Agent Architecture** — a protocol-first, artifact-first system where:

- **Agents are roles, not minds** — deterministic contracts, not creative actors
- **Files are system memory** — the repository is the single source of truth
- **CHECK protocol** — constitutional barrier that validates compliance before any task is marked done
- **OCCAM rules** — anti-entropy mechanism that keeps complexity justified

Key architectural documents live in `blocks/frameworks/`:
- `constitutional-agent-architecture.md`
- `agentic-repository-architecture-doctrine.md`
- `agent-roles-not-minds.md`
- `occam-rules-anti-entropy.md`

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/jirbis/knowledge-os.git
cd knowledge-os

# Initialize directory structure (if needed)
python3 tools/init_repository.py .

# Generate embeddings for existing blocks
python3 tools/embed_blocks.py

# Search your knowledge base
python3 tools/semantic_search.py -q "your query here"
```

---

## License

See repository for license details.

---
id: P1-003
type: P1            # standard changes; the deferred reuse-tracker is P2 and out of scope here
status: proposed
date: 2026-07-05
title: Provenance in block frontmatter and privacy-safe defaults
relates_to:
  - .cursor/commands/extract.md
  - config.yaml
  - tools/embed_blocks.py
  - tools/semantic_search.py
---

# P1-003 — Provenance and privacy defaults

## Summary

Blocks cannot currently be traced back to their source conversations, several
constitutional promises (traceability, confidence calibration, dedup-before-extract)
have no data to run on, and the default embeddings configuration sends private
knowledge to a third-party API. This proposal adds provenance fields to the block
schema, flips the privacy default, and pins dependencies.

## Findings and changes

### F1. No provenance — traceability is a dead letter (P1)

ASSEMBLE must "include source references", and the frontmatter schema records only
`source: chat` — no conversation id, no extraction date. A block can cite nothing,
and nothing can cite a block's origin.

**Change:** extend the block frontmatter schema with:

```yaml
id: <type>.<slug>            # stable block id, matches read_block.py addressing
extracted_at: <ISO-8601>
source: chat | <repo-name>
source_ref: <conversation_id or file#anchor>   # optional but recommended
```

EXTRACT fills these automatically; `tools/check.py` (P2-001) validates presence of
`id` and `extracted_at`.

### F2. Confidence calibration has no inputs (P1)

`organize.md` says: reused often → suggest raising confidence. Nothing tracks reuse —
the `used` lifecycle state is deprecated, and export documents are the only record.
`tools/assemble_blocks.py` already writes `source_blocks:` into every assembled
document's frontmatter, so the data exists on the export side.

**Change (minimal, no new moving part):** document in `organize.md` that reuse counts
are derived by scanning `export/*/frontmatter.source_blocks` at ORGANIZE time — a
read-only aggregation the Organizer performs, not a stored counter.
A dedicated reuse-tracking tool would be a new moving part → deferred to a future P2
proposal if the manual derivation proves insufficient.

### F3. Privacy default sends knowledge to a third party (P1)

`config.yaml` sets `embeddings.model: openai`. Every block — private, personal
knowledge — is sent to the OpenAI API by default, while `search.md` §Security demands
chat exports never be uploaded anywhere. The same data, one pipeline step later,
leaves the machine silently.

**Change:** default `embeddings.model: local` (sentence-transformers,
`all-MiniLM-L6-v2` — already supported by `embed_blocks.py`). `openai` becomes
explicit opt-in; `embed_blocks.py` prints a one-line notice when a remote model is
selected ("block content will be sent to <provider>").

### F4. Dedup-before-extract impossible on a fresh clone (P1)

The recommended practice "semantic search before extracting" depends on
`index/embeddings.sqlite`, which is gitignored and (today) OpenAI-dependent.
With F3's local default, any clone can rebuild the index offline:
document `python3 tools/embed_blocks.py` as a required post-clone step in README
(it already appears in Getting Started — mark it as the dedup prerequisite).

### F5. Dependencies unpinned, tools untested (P1)

~2,400 lines of Python, no `requirements.txt`, no tests. The two validator defects
proven in P2-001 would have been caught by trivial tests.

**Change:** add `requirements.txt` (pyyaml; extras documented for openai /
sentence-transformers) and a minimal `tests/` covering: boundary validator (allowlist,
intents, CWD-independence), frontmatter parsing in `read_block.py`, and ingest
idempotency in `ingest_chatgpt_export.py`. CI from P2-001 runs them.

## Occam note

New parts: one `requirements.txt`, one test module. The reuse-tracker explicitly NOT
added (OCCAM-1: necessity unproven while manual derivation suffices). Schema fields
are data, not machinery.

## Migration

Existing blocks lack the new fields. `id` and `extracted_at` become mandatory for
*new* blocks only; `tools/check.py` warns (not fails) on legacy blocks missing them.
No retroactive editing — blocks are append-only per constitution.

## Reversal plan

Schema fields are additive and ignorable; config default reverts via git; deleting
`tests/` and `requirements.txt` restores the status quo.

## Acceptance criteria

- [ ] New blocks created by EXTRACT carry `id`, `extracted_at`, and `source`.
- [ ] `config.yaml` defaults to local embeddings; remote models print a notice.
- [ ] Fresh clone can run dedup search fully offline.
- [ ] `pip install -r requirements.txt && pytest` passes in CI.

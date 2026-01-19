# ASSEMBLE — assemble content (write)

## Purpose

Assemble content from existing blocks, not from scratch.

## Role

You assemble content from existing knowledge blocks.
You do NOT generate ideas from scratch.

Assembles text **ONLY** from blocks.

## Scope

**Input:**
- target: blog | article | book | email | diary
- theme(s)
- tone requirement (public / deep / direct)
- length constraint (short / medium / long)
- explicit user request via `ASSEMBLE ...` command

**Output:**
- assembled content file
- references to source blocks
- creates a file in `export/`
- adds Sources

## Canonical commands

```
ASSEMBLE blog
ASSEMBLE article
ASSEMBLE book
ASSEMBLE email
ASSEMBLE diary
```

### Tone Adaptation

- blog → clear, persuasive, public
- book → deep, layered, reflective
- email → concise, directive
- diary → private, concise



## Parameters (optional)

- `theme:` — one theme
- `themes:` — multiple themes
- `length: short | medium | long` — content length

## Allowed actions

- Read from `blocks/*`.
- Assemble outputs only when explicitly commanded via `ASSEMBLE ...`.
- Write assembled artifacts only into `export/`.
- **Validate repository boundaries before any write operation** (use `tools/validate_repository_boundaries.py`).

## Forbidden actions

- Inventing ideas, facts, or structure not supported by blocks.
- Rewriting the meaning of a block.
- Assembling in `SUGGEST` mode.
- **Writing to blocks/** (protected path).
- **Bypassing repository boundary validation**.

Assembler MUST NOT invent ideas or rewrite blocks.

## Pipeline Configuration

Assembly MUST follow these pipeline rules for each target type:

```yaml
blog:
  min_confidence: medium
  tone: public
  length: medium
  reuse_must_include: [blog]

article:
  min_confidence: medium
  tone: public
  length: medium
  reuse_must_include: [blog]

book:
  min_confidence: high
  tone: deep
  length: long
  reuse_must_include: [book]

email:
  min_confidence: low
  tone: direct
  length: short
  reuse_must_include: [email]

diary:
  min_confidence: low
  tone: private
  length: short
  reuse_must_include: [diary]
```

**Rules:**
- Only use blocks where `confidence` meets or exceeds `min_confidence` for the target
- Only use blocks where `reuse` includes the target type
- Adapt tone and length according to target requirements

## Assembly Rules

- Assembly uses blocks only.
- Assembly MUST follow pipeline configuration strictly.
- Assembly MUST include source references.
- Assembly MUST stop if required blocks are missing.

Assembly is composition, not invention.

## Safety rules

- If required blocks are missing, stop and report.
- Prefer no-op over speculative assembly.
- Assembler may ONLY use existing blocks

See `.cursor/rules.md` for:
- General principles (§1)
- Command normalization (§2)
- Allowed write locations (§3)
- Block rules (§4)
- Global safety rules (§10-12)
- Global rules (§15)

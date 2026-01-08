# Required Fixes Checklist — AGENTS (Split Files)

This checklist enumerates **all required edits** to make the agent system
strict, unambiguous, and Cursor-safe.

The goal is:
- AGENTS are split into separate files
- Global rules live only in AGENTS.md
- Each agent has its own command contract

---

## 1️⃣ Split Agents into Separate Files (MANDATORY)

Create the following files:

- AGENTS/Extractor.md
- AGENTS/Organizer.md
- AGENTS/Assembler.md
- AGENTS/ArchiveSearch.md

`AGENTS.md` must remain **constitution-only** (no agent logic inside).

---

## 2️⃣ Update `AGENTS.md` (Global Constitution Only)

### Remove from AGENTS.md
- ❌ Any agent-specific logic
- ❌ Any command aliases
- ❌ Any operational instructions

### Keep in AGENTS.md
- ✅ Agent philosophy
- ✅ Source of truth hierarchy
- ✅ Command authority
- ✅ SUGGEST rules
- ✅ Safety & reversibility
- ✅ Evolution rules

### Add / Verify
- [ ] Explicit reference to `COMMANDS.md` as the only command source
- [ ] Explicit path to pipelines: `knowledge/pipelines/pipeline.yaml`
- [ ] List of official agents with one-line responsibility:
  - Extractor — knowledge extraction
  - Organizer — structure and hygiene
  - Assembler — content assembly
  - ArchiveSearch — archive indexing & search

---

## 3️⃣ Add `## Command normalization` to EACH Agent File (MANDATORY)

Each agent file MUST contain a dedicated section:

### Extractor.md
- Canonical:
  - `EXTRACT <type>`
  - `SUGGEST extract`
- Russian aliases:
  - `ИЗВЛЕЧЬ ...`
  - `ПРЕДЛОЖИ извлечение`

### Organizer.md
- Canonical:
  - `ORGANIZE ...`
  - `SUGGEST organization`
- Russian aliases:
  - `ОРГАНИЗОВАТЬ ...`
  - `ПРЕДЛОЖИ организацию`

### Assembler.md
- Canonical:
  - `ASSEMBLE <target>`
  - `SUGGEST assembly`
- Russian aliases:
  - `СОБРАТЬ ...`
  - `ПРЕДЛОЖИ сборку`

### ArchiveSearch.md
- Canonical:
  - `SEARCH archive`
- Russian aliases:
  - `ПОИСК архив`
  - `НАЙТИ в архиве`

---

## 4️⃣ Fix Assembler Source References (MANDATORY)

### Current problem
Assembler examples reference:
```
blocks/conclusions/...
```

### Required fix
Assembler MUST reference absolute repo paths:
```
knowledge/blocks/conclusions/...
knowledge/blocks/frameworks/...
```

This applies to:
- Sources section
- Error messages
- Missing-block reports

---

## 5️⃣ Clarify Pipeline Path (MANDATORY)

Anywhere pipelines are referenced, replace:
```
pipeline.yaml
```

with:
```
knowledge/pipelines/pipeline.yaml
```

This must be consistent across:
- AGENTS.md
- AGENTS/Assembler.md

---

## 6️⃣ Normalize Organizer Rules (STRUCTURAL FIX)

In `AGENTS/Organizer.md`, reformat:

### Required sections
- Tag normalization (MUST / MUST NOT)
- Theme hygiene rules
- Duplication handling rules
- Confidence calibration rules
- Forbidden actions

All rules must be explicit and list-based.

---

## 7️⃣ ArchiveSearch Safety Boundary (VERIFY)

In `AGENTS/ArchiveSearch.md`, verify:

- [ ] Allowed paths limited to `archive/` and `index/`
- [ ] Explicit prohibition on writing to:
  - `knowledge/blocks/`
  - `knowledge/candidates/`
  - `output/`
- [ ] Mandatory idempotent indexing rules

---

## 8️⃣ Final Consistency Check (DO NOT SKIP)

After changes:

- [ ] No agent logic remains in AGENTS.md
- [ ] Every agent file has `## Command normalization`
- [ ] Every command used is present in `COMMANDS.md`
- [ ] No relative-path ambiguity remains
- [ ] SUGGEST never writes files

---

## Definition of Done

The repository is correct if:
- Agents are deterministic
- Commands are explicit
- Archive is searchable but inert
- Knowledge is only created by EXTRACT / MARK
- Cursor behavior is predictable after weeks of inactivity

If any item above fails, fix structure — not prompts.


# One-Shot Commit Plan (Single Commit)

Goal: Split agents into separate files, clean AGENTS.md into a constitution-only doc,
and ensure COMMANDS/paths/normalization are consistent — in ONE commit.

---

## 0) Prep (no changes yet)
- Pull latest / ensure clean working tree:
  - `git status` must show no pending changes

---

## 1) Create folders (if missing)
Create:
- `AGENTS/`
- `knowledge/pipelines/`
- `tools/`
- `archive/exports/`
- `archive/normalized/`
- `index/`

(Only create folders that are missing.)

---

## 2) Move/split content into separate agent files
Create these new files (copy content from the current combined AGENTS doc, then trim):

1) `AGENTS/Extractor.md`
- Include: role, scope, block rules, file rules, frontmatter rules
- Add: `## Command normalization` (EXTRACT + SUGGEST extract + RU aliases)

2) `AGENTS/Organizer.md`
- Include: theme hygiene, duplication control, tag normalization, confidence calibration
- Add: `## Command normalization` (ORGANIZE + SUGGEST organization + RU aliases)
- Reformat rules into explicit MUST/MUST NOT bullets

3) `AGENTS/Assembler.md`
- Include: assembly-only rules, pipeline compliance, missing-block behavior, sources requirements
- Add: `## Command normalization` (ASSEMBLE + SUGGEST assembly + RU aliases)
- FIX: Sources paths must reference `knowledge/blocks/...`

4) `AGENTS/ArchiveSearch.md`
- Include: indexing rules, allowed paths, search output contract, failure handling
- Add: `## Command normalization` (SEARCH archive + RU aliases)

---

## 3) Rewrite `AGENTS.md` (constitution-only)
Replace the current `AGENTS.md` with:
- Agent philosophy
- Source-of-truth hierarchy
- Command authority + reference to `COMMANDS.md`
- Command normalization global rule (no alias list here)
- SUGGEST non-destructive rule
- Block/Candidate integrity rules
- Assembly rules
- Organizer authority
- Safety & reversibility
- Evolution rules
- Official agent list (1–2 lines per agent)

Mandatory fixes inside AGENTS.md:
- Mention pipeline path exactly: `knowledge/pipelines/pipeline.yaml`
- Do NOT include agent-specific alias tables

---

## 4) Update `COMMANDS.md`
Ensure it includes:
- EXTRACT + RU aliases
- MARK + RU aliases
- ORGANIZE + RU aliases
- ASSEMBLE + RU aliases
- SUGGEST + RU aliases
- STATUS + RU aliases
- SEARCH archive + RU aliases + behavior constraints

Also ensure:
- Only commands in COMMANDS.md are “real”
- Keep strict language: “must be exact, no freeform”

---

## 5) Add / verify pipeline path file
Ensure this exists:
- `knowledge/pipelines/pipeline.yaml`

If your pipeline file is elsewhere (e.g. in root), move it here and update references:
- AGENTS.md
- AGENTS/Assembler.md
- README.md (if mentioned)

---

## 6) Add / verify tools for archive indexing (optional but recommended)
If you are adopting ArchiveSearch now, ensure these exist:
- `tools/ingest_chatgpt_export.py`
- `tools/search_archive.py`
- `tools/extract_snippet.py`

(If you don’t want tools in the same commit, skip this step and do a second commit later.)

---

## 7) Sanity checks (before commit)
Run these checks:

### Structure checks
- `AGENTS.md` contains no “Extractor/Organizer/Assembler instructions”
- Each file in `AGENTS/*.md` contains a `## Command normalization` section

### Path checks
- Pipeline references use: `knowledge/pipelines/pipeline.yaml`
- Assembler Sources use: `knowledge/blocks/...`

### Command checks
- Every command mentioned in agent files exists in `COMMANDS.md`
- No “extra commands” exist outside `COMMANDS.md`

### Optional functional checks
```bash
python3 tools/search_archive.py --help
python3 tools/ingest_chatgpt_export.py --help
```
(If tools included)

---

## 8) Stage and commit (single commit)
Stage all changes:
```bash
git add AGENTS.md AGENTS/ COMMANDS.md knowledge/pipelines/pipeline.yaml README.md tools/ archive/ index/
```

Commit message (suggested):
```
refactor: split agents, formalize commands, add archive search contract
```

---

## 9) Definition of Done
The commit is correct if:
- AGENTS are split into separate files
- AGENTS.md is constitution-only
- COMMANDS.md is the single command source of truth
- Assembler references correct block paths
- Pipeline path is consistent everywhere
- SEARCH archive is documented and constrained

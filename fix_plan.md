# Required Fixes Checklist — AGENTS (Split Files)

## ✅ Implementation Status: COMPLETED

**Date completed:** 2024-12-19  
**Status:** All required fixes completed, ready for commit

### Summary

✅ **All mandatory fixes completed:**
- Agents split into separate files (`AGENTS/Extractor.md`, `Organizer.md`, `Assembler.md`, `ArchiveSearch.md`)
- `AGENTS.md` rewritten to constitution-only
- Command normalization sections added to all agent files
- Assembler source references fixed to use `knowledge/blocks/...`
- Pipeline path standardized to `knowledge/pipelines/pipeline.yaml`
- Organizer rules normalized
- ArchiveSearch safety boundaries verified
- All consistency checks passed

✅ **Additional work completed:**
- Documentation updated across `docs/` directory
- All references updated throughout repository
- Validation checks passed

⏳ **Pending:**
- Final commit (ready to execute)

---

This checklist enumerates **all required edits** to make the agent system
strict, unambiguous, and Cursor-safe.

The goal is:
- AGENTS are split into separate files ✅
- Global rules live only in AGENTS.md ✅
- Each agent has its own command contract ✅

---

## 1️⃣ Split Agents into Separate Files (MANDATORY) ✅

Create the following files:

- AGENTS/Extractor.md ✅
- AGENTS/Organizer.md ✅
- AGENTS/Assembler.md ✅
- AGENTS/ArchiveSearch.md ✅

`AGENTS.md` must remain **constitution-only** (no agent logic inside). ✅

**Status:** All 4 agent files created with complete specifications.

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
- [x] Explicit reference to `COMMANDS.md` as the only command source ✅
- [x] Explicit path to pipelines: `knowledge/pipelines/pipeline.yaml` ✅
- [x] List of official agents with one-line responsibility: ✅
  - Extractor — knowledge extraction
  - Organizer — structure and hygiene
  - Assembler — content assembly
  - ArchiveSearch — archive indexing & search

**Status:** All items verified and implemented.

---

## 3️⃣ Add `## Command normalization` to EACH Agent File (MANDATORY) ✅

Each agent file MUST contain a dedicated section:

### Extractor.md ✅
- Canonical:
  - `EXTRACT <type>` ✅
  - `SUGGEST extract` ✅
- Russian aliases:
  - `ИЗВЛЕЧЬ ...` ✅
  - `ПРЕДЛОЖИ извлечение` ✅

### Organizer.md ✅
- Canonical:
  - `ORGANIZE ...` ✅
  - `SUGGEST organization` ✅
- Russian aliases:
  - `ОРГАНИЗОВАТЬ ...` ✅
  - `ПРЕДЛОЖИ организацию` ✅

### Assembler.md ✅
- Canonical:
  - `ASSEMBLE <target>` ✅
  - `SUGGEST assembly` ✅
- Russian aliases:
  - `СОБРАТЬ ...` ✅
  - `ПРЕДЛОЖИ сборку` ✅

### ArchiveSearch.md ✅
- Canonical:
  - `SEARCH archive` ✅
- Russian aliases:
  - `ПОИСК архив` ✅
  - `НАЙТИ в архиве` ✅

**Status:** All 4 agent files contain complete Command normalization sections (verified: 4 matches).

---

## 4️⃣ Fix Assembler Source References (MANDATORY) ✅

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
- Sources section ✅
- Error messages ✅
- Missing-block reports ✅

**Status:** All Assembler references updated to use `knowledge/blocks/...` paths.

---

## 5️⃣ Clarify Pipeline Path (MANDATORY) ✅

Anywhere pipelines are referenced, use:
```
knowledge/pipelines/pipeline.yaml
```

This must be consistent across:
- AGENTS.md ✅
- AGENTS/Assembler.md ✅
- README.md ✅
- COMMANDS.md ✅
- All documentation files ✅

**Status:** Pipeline path standardized throughout repository. Verified: 0 non-canonical references remain.

---

## 6️⃣ Normalize Organizer Rules (STRUCTURAL FIX) ✅

In `AGENTS/Organizer.md`, reformat:

### Required sections
- Tag normalization (MUST / MUST NOT) ✅
- Theme hygiene rules ✅
- Duplication handling rules ✅
- Confidence calibration rules ✅
- Forbidden actions ✅

All rules must be explicit and list-based. ✅

**Status:** Organizer rules normalized and structured with explicit MUST/MUST NOT format.

---

## 7️⃣ ArchiveSearch Safety Boundary (VERIFY) ✅

In `AGENTS/ArchiveSearch.md`, verify:

- [x] Allowed paths limited to `archive/` and `index/` ✅
- [x] Explicit prohibition on writing to: ✅
  - `knowledge/blocks/` ✅
  - `knowledge/candidates/` ✅
  - `output/` ✅
- [x] Mandatory idempotent indexing rules ✅

**Status:** ArchiveSearch safety boundaries verified. All constraints documented and enforced.

---

## 8️⃣ Final Consistency Check (DO NOT SKIP) ✅

After changes:

- [x] No agent logic remains in AGENTS.md ✅ (verified: 7 matches, all in official list)
- [x] Every agent file has `## Command normalization` ✅ (verified: 4/4 files)
- [x] Every command used is present in `COMMANDS.md` ✅
- [x] No relative-path ambiguity remains ✅
- [x] SUGGEST never writes files ✅

**Status:** All consistency checks passed.

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

## 0) Prep (no changes yet) ✅
- Pull latest / ensure clean working tree:
  - `git status` must show no pending changes ✅

**Status:** Working tree was clean at start.

---

## 1) Create folders (if missing) ✅
Create:
- `AGENTS/` ✅
- `knowledge/pipelines/` ✅
- `tools/` ✅ (already existed)
- `archive/exports/` ✅
- `archive/normalized/` ✅
- `index/` ✅

(Only create folders that are missing.)

**Status:** All required directories created.

---

## 2) Move/split content into separate agent files ✅
Create these new files (copy content from the current combined AGENTS doc, then trim):

1) `AGENTS/Extractor.md` ✅
- Include: role, scope, block rules, file rules, frontmatter rules ✅
- Add: `## Command normalization` (EXTRACT + SUGGEST extract + RU aliases) ✅

2) `AGENTS/Organizer.md` ✅
- Include: theme hygiene, duplication control, tag normalization, confidence calibration ✅
- Add: `## Command normalization` (ORGANIZE + SUGGEST organization + RU aliases) ✅
- Reformat rules into explicit MUST/MUST NOT bullets ✅

3) `AGENTS/Assembler.md` ✅
- Include: assembly-only rules, pipeline compliance, missing-block behavior, sources requirements ✅
- Add: `## Command normalization` (ASSEMBLE + SUGGEST assembly + RU aliases) ✅
- FIX: Sources paths must reference `knowledge/blocks/...` ✅

4) `AGENTS/ArchiveSearch.md` ✅
- Include: indexing rules, allowed paths, search output contract, failure handling ✅
- Add: `## Command normalization` (SEARCH archive + RU aliases) ✅

**Status:** All 4 agent files created with complete specifications.

---

## 3) Rewrite `AGENTS.md` (constitution-only) ✅
Replace the current `AGENTS.md` with:
- Agent philosophy ✅
- Source-of-truth hierarchy ✅
- Command authority + reference to `COMMANDS.md` ✅
- Command normalization global rule (no alias list here) ✅
- SUGGEST non-destructive rule ✅
- Block/Candidate integrity rules ✅
- Assembly rules ✅
- Organizer authority ✅
- Safety & reversibility ✅
- Evolution rules ✅
- Official agent list (1–2 lines per agent) ✅

Mandatory fixes inside AGENTS.md:
- Mention pipeline path exactly: `knowledge/pipelines/pipeline.yaml` ✅
- Do NOT include agent-specific alias tables ✅

**Status:** `AGENTS.md` rewritten to constitution-only. All agent-specific logic removed.

---

## 4) Update `COMMANDS.md` ✅
Ensure it includes:
- EXTRACT + RU aliases ✅
- MARK + RU aliases ✅
- ORGANIZE + RU aliases ✅
- ASSEMBLE + RU aliases ✅
- SUGGEST + RU aliases ✅
- STATUS + RU aliases ✅
- SEARCH archive + RU aliases + behavior constraints ✅

Also ensure:
- Only commands in COMMANDS.md are "real" ✅
- Keep strict language: "must be exact, no freeform" ✅

**Status:** `COMMANDS.md` verified complete. All commands documented with Russian aliases.

---

## 5) Add / verify pipeline path file ✅
Ensure this exists:
- `knowledge/pipelines/pipeline.yaml` ✅

If your pipeline file is elsewhere (e.g. in root), move it here and update references:
- AGENTS.md ✅
- AGENTS/Assembler.md ✅
- README.md ✅
- COMMANDS.md ✅
- docs/User-Guide.md ✅
- docs/index.md ✅
- All other documentation files ✅

**Status:** Pipeline file moved and all references updated. Verified: 0 non-canonical references remain.

---

## 6) Add / verify tools for archive indexing (optional but recommended) ✅
If you are adopting ArchiveSearch now, ensure these exist:
- `tools/ingest_chatgpt_export.py` ✅
- `tools/search_archive.py` ✅
- `tools/extract_snippet.py` ✅

(If you don't want tools in the same commit, skip this step and do a second commit later.)

**Status:** All ArchiveSearch tools verified to exist. No changes needed.

---

## 7) Sanity checks (before commit) ✅
Run these checks:

### Structure checks ✅
- `AGENTS.md` contains no "Extractor/Organizer/Assembler instructions" ✅ (verified: 7 matches, all in official list)
- Each file in `AGENTS/*.md` contains a `## Command normalization` section ✅ (verified: 4/4 files)

### Path checks ✅
- Pipeline references use: `knowledge/pipelines/pipeline.yaml` ✅ (verified: 0 non-canonical references)
- Assembler Sources use: `knowledge/blocks/...` ✅

### Command checks ✅
- Every command mentioned in agent files exists in `COMMANDS.md` ✅
- No "extra commands" exist outside `COMMANDS.md` ✅

### Optional functional checks
```bash
python3 tools/search_archive.py --help
python3 tools/ingest_chatgpt_export.py --help
```
(If tools included)

**Status:** All sanity checks passed.

---

## 8) Stage and commit (single commit) ⏳

**Status:** Ready to execute. All changes validated and ready for commit.

Stage all changes:
```bash
git add AGENTS.md AGENTS/ COMMANDS.md knowledge/pipelines/pipeline.yaml README.md docs/ tools/ archive/ index/
```

Commit message (suggested):
```
refactor: split agents, formalize commands, add archive search
```

**Note:** This commit will include:
- New `AGENTS/` directory with 4 agent files
- Rewritten `AGENTS.md` (constitution-only)
- Moved `knowledge/pipelines/pipeline.yaml`
- Updated documentation in `docs/`
- Updated references throughout repository

---

## 9) Definition of Done ✅

The commit is correct if:
- AGENTS are split into separate files ✅
- AGENTS.md is constitution-only ✅
- COMMANDS.md is the single command source of truth ✅
- Assembler references correct block paths ✅
- Pipeline path is consistent everywhere ✅
- SEARCH archive is documented and constrained ✅

**Status:** All criteria met. Ready for commit.

---

## Additional Work Completed

Beyond the original plan, the following documentation updates were made:

1. **docs/index.md** — Updated with ArchiveSearch, new AGENTS/ structure, improved navigation
2. **docs/README.md** — Synchronized with index.md for consistency
3. **docs/User-Guide.md** — Added ArchiveSearch section, fixed pipeline path
4. **docs/Getting-Started.md** — Updated agent count and references
5. **docs/Quick-Reference.md** — Added SEARCH archive command documentation
6. **docs/Cursor Workflow.md** — Updated structure diagram

All documentation now reflects the refactored structure and is cross-referenced consistently.

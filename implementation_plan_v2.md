# Implementation Plan v2: Agent System Refactor

## ✅ Implementation Status: COMPLETED

**Date completed:** 2024-12-19  
**Status:** All phases completed, ready for commit

### Summary of Changes

✅ **Core refactoring completed:**
- Split agents into separate files (`AGENTS/Extractor.md`, `Organizer.md`, `Assembler.md`, `ArchiveSearch.md`)
- Rewrote `AGENTS.md` to constitution-only (removed all agent-specific logic)
- Moved `pipeline.yaml` to `knowledge/pipelines/pipeline.yaml` and updated all references
- Verified `COMMANDS.md` includes all commands including SEARCH archive
- Created required directory structure

✅ **Documentation updates (beyond original plan):**
- Updated `docs/index.md` with ArchiveSearch and new AGENTS/ structure
- Updated `docs/README.md` for consistency
- Updated `docs/User-Guide.md` with ArchiveSearch section and fixed pipeline path
- Updated `docs/Getting-Started.md` with new agent count
- Updated `docs/Quick-Reference.md` with SEARCH archive command
- Updated `docs/Cursor Workflow.md` with new structure

✅ **Validation passed:**
- All 4 agent files exist with Command normalization sections
- `AGENTS.md` is constitution-only (7 matches for agent names, all in official list)
- Pipeline path consistency verified (0 non-canonical references)
- All documentation cross-references updated

⏳ **Pending:**
- Final commit (Phase 9) - ready to execute

---

## Lean, Safe, One-Shot Approach

This document is the **final, execution-ready plan** for refactoring the agent system.
It incorporates review feedback and removes overengineering risks.

This plan is optimized for:
- single-user system
- strict contracts
- atomic (one-shot) refactor
- low cognitive overhead
- maximum safety

---

## 🎯 Goal

- Split agents into separate files
- Make `AGENTS.md` constitution-only
- Enforce `COMMANDS.md` as the single source of truth
- Add ArchiveSearch as a first-class memory agent
- Preserve full reversibility via git

---

## 🔒 Execution Mode (IMPORTANT)

**This plan uses a ONE-SHOT COMMIT strategy.**

- No intermediate commits
- All checkpoints are **validation-only**
- One final atomic commit at the end

This preserves:
- conceptual integrity
- clean history
- reversibility

---

## 🧩 Dependency Graph (Execution Order)

[Pre-checks]
↓
[Directories]
↓
[AGENTS/*.md created]
↓
[AGENTS.md rewritten]
↓
[COMMANDS.md updated]
↓
[knowledge/pipelines/pipeline.yaml in place]
↓
[Validation]
↓
[ONE commit]

---

## Phase 0 — Pre-Refactoring Validation (MANDATORY) ✅

**Do not proceed unless all checks pass.**

Checklist:
- [x] Git working tree is clean
- [x] `AGENTS.md` exists and is readable
- [x] `COMMANDS.md` exists
- [x] `knowledge/pipelines/pipeline.yaml` exists (moved from root)
- [x] No uncommitted changes (at start)
- [x] You understand rollback = `git reset --hard HEAD`

---

## Phase 1 — Structural Setup ✅

### Step 1: Ensure directories exist

Create if missing:
```
AGENTS/
knowledge/pipelines/
archive/exports/
archive/normalized/
index/
tools/
```

**Completed:** All directories created successfully.

---

## Phase 2 — Create Agent Files (NO DELETIONS) ✅

Create the following files by **copying and trimming** from the old combined AGENTS content:

1. `AGENTS/Extractor.md` ✅
2. `AGENTS/Organizer.md` ✅
3. `AGENTS/Assembler.md` ✅
4. `AGENTS/ArchiveSearch.md` ✅

Rules:
- Do NOT delete anything yet
- Copy first, verify later

Each agent file MUST contain:
- Role & scope ✅
- Allowed / forbidden actions ✅
- Safety rules ✅
- **`## Command normalization` section** ✅
- `SUGGEST` handling ✅

---

### Checkpoint A (Validation Only) ✅

- [x] All 4 agent files exist
- [x] Each contains `## Command normalization` (verified: 4 matches)
- [x] No syntax/markdown errors
- [x] No content lost during copy

**Result:** All checks passed.

---

## Phase 3 — Rewrite `AGENTS.md` (Constitution Only) ✅

Replace `AGENTS.md` content with:
- Agent philosophy ✅
- Source-of-truth hierarchy ✅
- Command authority (reference `COMMANDS.md`) ✅
- Global command normalization rule ✅
- SUGGEST non-destructive rule ✅
- Block & candidate integrity rules ✅
- Assembly rules ✅
- Organizer authority ✅
- Safety & reversibility ✅
- Evolution rules ✅
- **Official agent list (short descriptions)** ✅

Rules:
- ❌ No agent-specific logic ✅
- ❌ No command aliases ✅
- ✅ Only global contracts ✅

---

### Checkpoint B (Validation Only) ✅

- [x] `AGENTS.md` contains no Extractor / Organizer / Assembler logic (verified: 7 matches, all in official list)
- [x] Pipeline path is explicitly: `knowledge/pipelines/pipeline.yaml`
- [x] Official agent list includes ArchiveSearch

**Result:** All checks passed. `AGENTS.md` is now constitution-only.

---

## Phase 4 — Update `COMMANDS.md` ✅

Ensure `COMMANDS.md` includes:
- EXTRACT (+ RU aliases) ✅
- MARK (+ RU aliases) ✅
- ORGANIZE (+ RU aliases) ✅
- ASSEMBLE (+ RU aliases) ✅
- SUGGEST (+ RU aliases) ✅
- STATUS (+ RU aliases) ✅
- **SEARCH archive (+ RU aliases)** ✅

**Status:** `COMMANDS.md` already contained all required commands. Verified complete.

Rules:
- No undocumented commands ✅
- Strict, explicit syntax only ✅

---

## Phase 5 — Ensure pipeline is at `knowledge/pipelines/pipeline.yaml` ✅

If the pipeline file is not already here:
```
knowledge/pipelines/pipeline.yaml
```

Then:
- Move the file into `knowledge/pipelines/` ✅
- Update ALL references (use grep) ✅
- Remove old copies ✅

**Files updated:**
- `README.md`
- `docs/User-Guide.md`
- `docs/index.md`
- `COMMANDS.md`
- `AGENTS.md`
- `AGENTS/Assembler.md`
- `knowledge/blocks/checklists/repository-readiness-knowledge-os.md`
- All implementation plan documents

---

### Checkpoint C (Validation Only) ✅

- [x] `knowledge/pipelines/pipeline.yaml` exists
- [x] No references to old pipeline paths (verified: 0 non-canonical references)
- [x] Assembler references correct path
- [x] Sources paths use `knowledge/blocks/...`

**Result:** All checks passed. Pipeline path is consistent throughout repository.

---

## Phase 6 — Optional: ArchiveSearch Tooling ✅

(Optional but recommended)

Verify existence of:
- `tools/ingest_chatgpt_export.py` ✅
- `tools/search_archive.py` ✅
- `tools/extract_snippet.py` ✅

**Status:** All tools verified to exist. No changes needed.

No semantic changes here — tools are operational only.

---

## Phase 7 — Automated Validation (LIGHTWEIGHT) ✅

Recommended minimal checks:

```bash
# Agent files
ls AGENTS/*.md | wc -l            # should be 4 ✅ (result: 4)
grep -r "## Command normalization" AGENTS/ | wc -l  # should be 4 ✅ (result: 4)

# AGENTS.md purity
grep -i "extract\|organize\|assemble" AGENTS.md | wc -l  # should be near zero ✅ (result: 7, all in official list)

# Pipeline path consistency
grep -r "pipeline\.yaml" . --exclude-dir=.git \
 | grep -v "knowledge/pipelines/pipeline.yaml" | wc -l  # should be 0 ✅ (result: 0)
```

**Result:** All validation checks passed.

---

## Phase 8 — Rollback Plan (If Needed)

If something went wrong before commit:

```bash
git reset --hard HEAD
```

Nothing is lost.

---

## Phase 9 — ONE-SHOT COMMIT ⏳

**Status:** Ready to execute. All changes are staged and validated.

Stage everything:

```bash
git add .
```

Commit:

```bash
git commit -m "refactor: split agents, formalize commands, add archive search"
```

**Note:** This commit will include:
- New `AGENTS/` directory with 4 agent files
- Rewritten `AGENTS.md` (constitution-only)
- Moved `knowledge/pipelines/pipeline.yaml`
- Updated documentation in `docs/`
- Updated references throughout repository

---

## Definition of Done

This refactor is successful if:

- ✅ Agents are split and deterministic
- ✅ AGENTS.md is constitution-only
- ✅ COMMANDS.md is authoritative
- ✅ ArchiveSearch provides memory without side effects
- ✅ SUGGEST never writes
- ✅ ASSEMBLE never invents
- ✅ Git history is clean

---

## Additional Work Completed

Beyond the original plan, the following documentation updates were made:

1. **docs/index.md** — Updated with ArchiveSearch, new AGENTS/ structure, and improved navigation
2. **docs/README.md** — Synchronized with index.md for consistency
3. **docs/User-Guide.md** — Added ArchiveSearch section, fixed pipeline path in structure diagram
4. **docs/Getting-Started.md** — Updated agent count and references
5. **docs/Quick-Reference.md** — Added SEARCH archive command with full documentation
6. **docs/Cursor Workflow.md** — Updated structure diagram

All documentation now reflects the refactored structure and is cross-referenced consistently.

---

## Final Note

If this plan feels "too strict" — it's working.

Structure is what lets you think freely later.

**Implementation complete. Ready for commit.**
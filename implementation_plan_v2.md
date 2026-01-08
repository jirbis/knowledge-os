# Implementation Plan v2: Agent System Refactor

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
[pipeline.yaml moved]
↓
[Validation]
↓
[ONE commit]

---

## Phase 0 — Pre-Refactoring Validation (MANDATORY)

**Do not proceed unless all checks pass.**

Checklist:
- [ ] Git working tree is clean
- [ ] `AGENTS.md` exists and is readable
- [ ] `COMMANDS.md` exists
- [ ] `pipeline.yaml` exists (root or known location)
- [ ] No uncommitted changes
- [ ] You understand rollback = `git reset --hard HEAD`

---

## Phase 1 — Structural Setup

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

---

## Phase 2 — Create Agent Files (NO DELETIONS)

Create the following files by **copying and trimming** from the old combined AGENTS content:

1. `AGENTS/Extractor.md`
2. `AGENTS/Organizer.md`
3. `AGENTS/Assembler.md`
4. `AGENTS/ArchiveSearch.md`

Rules:
- Do NOT delete anything yet
- Copy first, verify later

Each agent file MUST contain:
- Role & scope
- Allowed / forbidden actions
- Safety rules
- **`## Command normalization` section**
- `SUGGEST` handling

---

### Checkpoint A (Validation Only)

- [ ] All 4 agent files exist
- [ ] Each contains `## Command normalization`
- [ ] No syntax/markdown errors
- [ ] No content lost during copy

If any check fails → fix before continuing.

---

## Phase 3 — Rewrite `AGENTS.md` (Constitution Only)

Replace `AGENTS.md` content with:
- Agent philosophy
- Source-of-truth hierarchy
- Command authority (reference `COMMANDS.md`)
- Global command normalization rule
- SUGGEST non-destructive rule
- Block & candidate integrity rules
- Assembly rules
- Organizer authority
- Safety & reversibility
- Evolution rules
- **Official agent list (short descriptions)**

Rules:
- ❌ No agent-specific logic
- ❌ No command aliases
- ✅ Only global contracts

---

### Checkpoint B (Validation Only)

- [ ] `AGENTS.md` contains no Extractor / Organizer / Assembler logic
- [ ] Pipeline path is explicitly: `knowledge/pipelines/pipeline.yaml`
- [ ] Official agent list includes ArchiveSearch

---

## Phase 4 — Update `COMMANDS.md`

Ensure `COMMANDS.md` includes:
- EXTRACT (+ RU aliases)
- MARK (+ RU aliases)
- ORGANIZE (+ RU aliases)
- ASSEMBLE (+ RU aliases)
- SUGGEST (+ RU aliases)
- STATUS (+ RU aliases)
- **SEARCH archive (+ RU aliases)**

Rules:
- No undocumented commands
- Strict, explicit syntax only

---

## Phase 5 — Move `pipeline.yaml`

If `pipeline.yaml` is not already here:
```
knowledge/pipelines/pipeline.yaml
```

Then:
- Move the file
- Update ALL references (use grep)
- Remove old copies

---

### Checkpoint C (Validation Only)

- [ ] `knowledge/pipelines/pipeline.yaml` exists
- [ ] No references to old pipeline paths
- [ ] Assembler references correct path
- [ ] Sources paths use `knowledge/blocks/...`

---

## Phase 6 — Optional: ArchiveSearch Tooling

(Optional but recommended)

Verify existence of:
- `tools/ingest_chatgpt_export.py`
- `tools/search_archive.py`
- `tools/extract_snippet.py`

No semantic changes here — tools are operational only.

---

## Phase 7 — Automated Validation (LIGHTWEIGHT)

Recommended minimal checks:

```bash
# Agent files
ls AGENTS/*.md | wc -l            # should be 4
grep -r "## Command normalization" AGENTS/ | wc -l  # should be 4

# AGENTS.md purity
grep -i "extract\|organize\|assemble" AGENTS.md | wc -l  # should be near zero

# Pipeline path consistency
grep -r "pipeline\.yaml" . --exclude-dir=.git \
 | grep -v "knowledge/pipelines/pipeline.yaml" | wc -l  # should be 0
```

---

## Phase 8 — Rollback Plan (If Needed)

If something went wrong before commit:

```bash
git reset --hard HEAD
```

Nothing is lost.

---

## Phase 9 — ONE-SHOT COMMIT

Stage everything:

```bash
git add .
```

Commit:

```bash
git commit -m "refactor: split agents, formalize commands, add archive search"
```

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

## Final Note

If this plan feels "too strict" — it's working.

Structure is what lets you think freely later.
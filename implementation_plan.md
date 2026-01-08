# Implementation Plan: Agent System Refactoring

This document provides a detailed change plan for all affected files according to `fix_plan.md`.

---

## 📋 Overview

**Goal:** Split agents into separate files, make AGENTS.md constitution-only, ensure path consistency, and formalize commands.

**Affected Files:**
- New files: 4 agent files in `AGENTS/`
- Modified files: `AGENTS.md`, `README.md`, `pipeline.yaml` (move)
- Verified files: `COMMANDS.md`, documentation files

---

## 🗂️ Step 1: Create Directory Structure

### Files to Create

```
AGENTS/
  Extractor.md
  Organizer.md
  Assembler.md
  ArchiveSearch.md

knowledge/
  pipelines/
    pipeline.yaml (move from root)
```

### Action Items

- [ ] Create `AGENTS/` directory
- [ ] Create `knowledge/pipelines/` directory (if missing)
- [ ] Move `pipeline.yaml` from root to `knowledge/pipelines/pipeline.yaml`

---

## 📝 Step 2: Create `AGENTS/Extractor.md`

### Source Content
Extract from current `AGENTS.md` lines 1-73.

### Required Sections

1. **Role** (from AGENTS.md:1-6)
   - Extract durable knowledge
   - Do NOT summarize chats
   - Create reusable blocks

2. **Scope** (from AGENTS.md:8-14)
   - Input: conversation context, user signals
   - Output: files in `knowledge/blocks/`

3. **What you extract** (from AGENTS.md:16-23)
   - Clear conclusion
   - Reusable framework
   - Checklist or decision rule
   - Strong metaphor or narrative

4. **Block types** (from AGENTS.md:25-30)
   - conclusion, framework, checklist, narrative, metaphor

5. **File rules** (from AGENTS.md:35-44)
   - One block → one file
   - Semantic filenames
   - Kebab-case
   - No dates

6. **Frontmatter (mandatory)** (from AGENTS.md:46-64)
   - Complete YAML template

7. **Content rules** (from AGENTS.md:66-77)
   - No fluff, no marketing
   - Write for blind reuse
   - Prefer principles

8. **Command normalization** (NEW - MANDATORY)
   ```markdown
   ## Command normalization
   
   ### Canonical commands
   - EXTRACT conclusion
   - EXTRACT framework
   - EXTRACT checklist
   - EXTRACT narrative
   - EXTRACT metaphor
   - SUGGEST extract
   
   ### Russian aliases
   - ИЗВЛЕЧЬ вывод → EXTRACT conclusion
   - ИЗВЛЕЧЬ фреймворк → EXTRACT framework
   - ИЗВЛЕЧЬ чеклист → EXTRACT checklist
   - ИЗВЛЕЧЬ рассказ → EXTRACT narrative
   - ИЗВЛЕЧЬ метафору → EXTRACT metaphor
   - ПРЕДЛОЖИ извлечение → SUGGEST extract
   
   ### Rules
   - Matching is case-insensitive
   - Commands must be exact (no declension, no extra words)
   - Natural language requests MUST NOT be interpreted as commands
   ```

### Action Items

- [ ] Create `AGENTS/Extractor.md`
- [ ] Copy relevant sections from `AGENTS.md`
- [ ] Add `## Command normalization` section
- [ ] Verify all commands exist in `COMMANDS.md`

---

## 📝 Step 3: Create `AGENTS/Organizer.md`

### Source Content
Extract from current `AGENTS.md` lines 74-153.

### Required Sections

1. **Role** (from AGENTS.md:76-78)
   - Maintain coherence
   - Prevent duplication
   - Prevent thematic chaos

2. **Scope** (from AGENTS.md:80-94)
   - Input: existing blocks, new blocks, user requests
   - Output: updated metadata, merged/deprecated blocks

3. **Core responsibilities** (from AGENTS.md:90-152)
   - **Theme hygiene** (MUST/MUST NOT format)
     - Each block must have 1 primary theme
     - Max 2 themes per block
     - Themes must be stable concepts, not projects
     - Good themes: ai-agents, executable-protocols, jira-decline
     - Bad themes: client-x, january-notes, random-thoughts
   
   - **Duplication control** (MUST/MUST NOT format)
     - If two blocks express same idea → propose merge
     - Keep stronger one, deprecate other
     - Deprecated block format
   
   - **Tag normalization** (MUST/MUST NOT format)
     - Enforce canonical tag list
     - Map synonyms → canonical tags
     - Max 10 tags per block
   
   - **Confidence calibration** (MUST/MUST NOT format)
     - If reused often → suggest confidence increase
     - If speculative → downgrade to low

4. **Forbidden actions** (from AGENTS.md:141-147)
   - Do NOT rewrite content unless asked
   - Do NOT invent new themes
   - Do NOT delete files

5. **Organizer mindset** (from AGENTS.md:149-152)
   - Librarian, not author
   - Structure beats cleverness

6. **Command normalization** (NEW - MANDATORY)
   ```markdown
   ## Command normalization
   
   ### Canonical commands
   - ORGANIZE knowledge blocks
   - ORGANIZE themes
   - ORGANIZE duplicates
   - SUGGEST organization
   
   ### Russian aliases
   - ОРГАНИЗОВАТЬ блоки → ORGANIZE knowledge blocks
   - ОРГАНИЗОВАТЬ темы → ORGANIZE themes
   - ОРГАНИЗОВАТЬ дубликаты → ORGANIZE duplicates
   - ПРЕДЛОЖИ организацию → SUGGEST organization
   
   ### Rules
   - Commands must be explicit and imperative
   - Organizer never runs automatically on vague requests
   - If scope is unclear, ask which dimension to organize
   ```

### Action Items

- [ ] Create `AGENTS/Organizer.md`
- [ ] Copy relevant sections from `AGENTS.md`
- [ ] Reformat rules into explicit MUST/MUST NOT bullets
- [ ] Add `## Command normalization` section
- [ ] Verify all commands exist in `COMMANDS.md`

---

## 📝 Step 4: Create `AGENTS/Assembler.md`

### Source Content
Extract from current `AGENTS.md` lines 157-228.

### Required Sections

1. **Role** (from AGENTS.md:161-165)
   - Assemble content from existing blocks
   - Do NOT generate ideas from scratch

2. **Scope** (from AGENTS.md:167-176)
   - Input: target, theme(s), tone, length
   - Output: assembled content file, source references

3. **Assembly rules** (from AGENTS.md:178-216)
   - **Source of truth** (FIX PATHS)
     - You may ONLY use: `knowledge/blocks/*`
     - Explicit user-provided text
     - If blocks insufficient → stop and report
   
   - **Assembly logic**
     - conclusions → core claims
     - frameworks → structure
     - checklists → actionable sections
     - narratives → transitions
   
   - **Reuse awareness**
     - Respect `reuse:` field in frontmatter
     - If block not allowed for target → skip it
   
   - **Traceability (mandatory)** (FIX PATHS)
     - At end of document, include:
     ```markdown
     ---
     Sources:
     - knowledge/blocks/conclusions/...
     - knowledge/blocks/frameworks/...
     ---
     ```
   
   - **Tone adaptation**
     - blog → clear, persuasive, public
     - book → deep, layered, reflective
     - email → concise, directive
     - Never change meaning, only adapt wording

4. **Pipeline compliance** (NEW - MANDATORY)
   - Assembly MUST follow `knowledge/pipelines/pipeline.yaml` strictly
   - If pipeline file missing → stop and report

5. **Forbidden actions** (from AGENTS.md:218-222)
   - No hallucinated insights
   - No rewriting history
   - No mixing incompatible themes

6. **Assembler mindset** (from AGENTS.md:224-228)
   - Builder, not author
   - Blocks are bricks
   - Composition, not invention

7. **Command normalization** (NEW - MANDATORY)
   ```markdown
   ## Command normalization
   
   ### Canonical commands
   - ASSEMBLE blog
   - ASSEMBLE article
   - ASSEMBLE book
   - ASSEMBLE email
   - SUGGEST assembly
   
   ### Russian aliases
   - СОБРАТЬ пост → ASSEMBLE blog
   - СОБРАТЬ статью → ASSEMBLE article
   - СОБРАТЬ книгу → ASSEMBLE book
   - СОБРАТЬ письмо → ASSEMBLE email
   - ПРЕДЛОЖИ сборку → SUGGEST assembly
   
   ### Rules
   - Assembly MUST follow knowledge/pipelines/pipeline.yaml strictly
   - Assembler may ONLY use existing blocks and candidates
   - If required blocks are missing, stop and report
   ```

### Critical Fixes

- [ ] **FIX:** All source references must use `knowledge/blocks/...` (not `blocks/...`)
- [ ] **FIX:** Pipeline path must be `knowledge/pipelines/pipeline.yaml`
- [ ] **FIX:** Error messages must use absolute paths

### Action Items

- [ ] Create `AGENTS/Assembler.md`
- [ ] Copy relevant sections from `AGENTS.md`
- [ ] Fix all path references to use `knowledge/blocks/...`
- [ ] Add pipeline compliance section
- [ ] Add `## Command normalization` section
- [ ] Verify all commands exist in `COMMANDS.md`

---

## 📝 Step 5: Create `AGENTS/ArchiveSearch.md`

### Source Content
Extract from current `AGENTS.md` lines 377-527.

### Required Sections

1. **Role** (from AGENTS.md:377-387)
   - Search ChatGPT exports with FTS5 indexing
   - Read-only with respect to `knowledge/blocks/`
   - May create/update only in `archive/` and `index/`

2. **Purpose** (from AGENTS.md:380-384)
   - Ensure SQLite FTS5 index exists and is up to date
   - Run full-text search query
   - Return ranked results + next-step commands

3. **Inputs (required)** (from AGENTS.md:391-399)
   - `export_path`: path to `conversations.json`
   - `query`: FTS search query string
   - `limit`: integer (default 20)
   - `reindex`: boolean (default false)

4. **Repository Paths (fixed)** (from AGENTS.md:403-413)
   - DB path: `index/chats.sqlite`
   - Normalized markdown dir: `archive/normalized/`
   - Export copy dir: `archive/exports/`
   - Scripts: `tools/ingest_chatgpt_export.py`, `tools/search_archive.py`, `tools/extract_snippet.py`

5. **Operating Rules** (from AGENTS.md:417-500)
   - **Non-destructive**
     - Never modify `knowledge/blocks/`, `knowledge/candidates/`, `output/`
     - Only create/update: `index/chats.sqlite`, `archive/normalized/*`
   
   - **Idempotent indexing**
     - Indexing required if: `reindex=true`, DB missing, DB older than export, tables missing
   
   - **Indexing command**
     ```bash
     python3 tools/ingest_chatgpt_export.py \
       --input "<export_path>" \
       --db "index/chats.sqlite" \
       --normalized-dir "archive/normalized"
     ```
   
   - **Search command**
     ```bash
     python3 tools/search_archive.py \
       --db "index/chats.sqlite" \
       --q "<query>" \
       --limit <limit>
     ```
   
   - **Output format**
     - Index status
     - Search results (ranked)
     - Next-step commands

6. **Error handling** (from AGENTS.md:492-500)
   - Show exact command that failed
   - Show stderr/stdout excerpt
   - Propose minimal fix

7. **FTS Query Tips** (from AGENTS.md:502-512)
   - Exact phrase, Boolean, Proximity, Exclude examples

8. **Security & Privacy** (from AGENTS.md:514-520)
   - Treat `conversations.json` as sensitive
   - Do not upload anywhere
   - Use snippets, not long dumps

9. **Command normalization** (NEW - MANDATORY)
   ```markdown
   ## Command normalization
   
   ### Canonical commands
   - SEARCH archive
   
   ### Russian aliases
   - ПОИСК архив → SEARCH archive
   - НАЙТИ в архиве → SEARCH archive
   
   ### Rules
   - SEARCH never creates knowledge blocks
   - SEARCH only finds raw material for SUGGEST / EXTRACT
   - Allowed paths: archive/, index/
   - Forbidden paths: knowledge/blocks/, knowledge/candidates/, output/
   ```

### Action Items

- [ ] Create `AGENTS/ArchiveSearch.md`
- [ ] Copy relevant sections from `AGENTS.md`
- [ ] Verify safety boundaries are explicit
- [ ] Add `## Command normalization` section
- [ ] Verify command exists in `COMMANDS.md`

---

## 📝 Step 6: Rewrite `AGENTS.md` (Constitution Only)

### Remove from AGENTS.md

- ❌ All agent-specific logic (Extractor, Organizer, Assembler, ArchiveSearch)
- ❌ All command aliases (move to individual agent files)
- ❌ All operational instructions (move to individual agent files)
- ❌ All examples of agent behavior (move to individual agent files)

### Keep in AGENTS.md

From current `AGENTS.md` lines 240-374:

1. **Title and Introduction** (NEW)
   ```markdown
   # Knowledge Operating System — Agent Constitution
   
   This file defines the global rules and contracts
   for all agents operating in this repository.
   
   If something is not allowed here, it is forbidden everywhere.
   ```

2. **Agent Philosophy** (from AGENTS.md:249-262)
   - Agents are: deterministic, non-creative, contract-driven
   - Agents are NOT: authors, brainstormers, chat companions
   - Creativity exists only in chat
   - Agents operate on files

3. **Source of Truth Hierarchy** (from AGENTS.md:266-276)
   - knowledge/blocks/ — atomic truth
   - knowledge/candidates/ — content intent
   - knowledge/pipelines/ — routing rules
   - output/ — generated artifacts
   - chat history — ephemeral, non-authoritative

4. **Command Authority** (from AGENTS.md:280-285, UPDATE)
   - Only commands defined in `COMMANDS.md` are valid
   - Natural language MUST NOT trigger actions
   - If command malformed → ask for clarification
   - **ADD:** Explicit reference to `COMMANDS.md` as single source of truth

5. **Command Normalization** (from AGENTS.md:289-297, SIMPLIFY)
   - Agents MUST normalize Russian aliases into canonical English commands
   - Normalization MUST happen before execution
   - If normalization fails → stop
   - **REMOVE:** Specific alias examples (move to agent files)

6. **SUGGEST Mode (Advisory Only)** (from AGENTS.md:301-307)
   - SUGGEST NEVER creates or modifies files
   - SUGGEST may analyze context and propose actions
   - SUGGEST MUST ask for explicit confirmation

7. **Block Integrity Rules** (from AGENTS.md:311-319)
   - One block = one idea
   - Blocks MUST NOT be edited for style during extraction
   - Blocks MUST be reusable without context
   - Blocks MUST contain frontmatter
   - Deletion forbidden, only deprecation allowed

8. **Candidate Integrity Rules** (from AGENTS.md:323-330)
   - Candidates reference blocks; they do not duplicate content
   - Candidates define structure and intent, not prose
   - Lifecycle: draft → solid → used → deprecated
   - Agents MUST respect candidate status

9. **Assembly Rules** (from AGENTS.md:334-341, UPDATE)
   - Assembly uses blocks and candidates only
   - Assembly MUST follow `knowledge/pipelines/pipeline.yaml` (FIX PATH)
   - Assembly MUST include source references
   - Assembly MUST stop if required blocks are missing
   - Assembly is composition, not invention

10. **Organizer Authority** (from AGENTS.md:345-350)
    - May suggest merges, deprecations, renames
    - MUST NOT apply destructive changes automatically
    - MUST explain rationale for every suggestion

11. **Safety and Reversibility** (from AGENTS.md:354-358)
    - All operations must be reversible via git
    - Agents MUST prefer no-op over risky action
    - Ambiguity → stop

12. **Evolution Rules** (from AGENTS.md:362-366)
    - New commands require updating `COMMANDS.md`
    - New agent behaviors require updating this file
    - Silent behavior changes are forbidden

13. **One Rule Above All** (from AGENTS.md:370-374)
    - If it is not in a block, it does not exist
    - Agents exist to protect this rule

14. **Official Agent List** (NEW - MANDATORY)
    ```markdown
    ## Official Agents
    
    This repository defines the following agents:
    
    - **Extractor** — Extracts durable knowledge from conversations into reusable blocks
    - **Organizer** — Maintains knowledge base coherence, prevents duplication, normalizes themes and tags
    - **Assembler** — Assembles content from existing blocks following pipeline rules
    - **ArchiveSearch** — Indexes and searches ChatGPT exports (read-only, does not create blocks)
    
    For agent-specific instructions, see:
    - `AGENTS/Extractor.md`
    - `AGENTS/Organizer.md`
    - `AGENTS/Assembler.md`
    - `AGENTS/ArchiveSearch.md`
    
    For command specifications, see `COMMANDS.md`.
    ```

### Critical Fixes

- [ ] **FIX:** Pipeline path must be `knowledge/pipelines/pipeline.yaml` (not `pipeline.yaml`)
- [ ] **ADD:** Explicit reference to `COMMANDS.md`
- [ ] **ADD:** Official agent list with responsibilities
- [ ] **REMOVE:** All agent-specific logic

### Action Items

- [ ] Rewrite `AGENTS.md` with constitution-only content
- [ ] Fix pipeline path reference
- [ ] Add official agent list
- [ ] Remove all agent-specific sections
- [ ] Verify structure matches requirements

---

## 📝 Step 7: Update `README.md`

### Changes Required

1. **Pipeline Path Reference** (if mentioned)
   - Find: `pipeline.yaml`
   - Replace: `knowledge/pipelines/pipeline.yaml`

2. **Agent References** (if mentioned)
   - Update to reference `AGENTS/` directory structure
   - Or keep generic reference to `AGENTS.md` (constitution)

### Action Items

- [ ] Search for `pipeline.yaml` references
- [ ] Update to `knowledge/pipelines/pipeline.yaml`
- [ ] Verify agent references are correct
- [ ] Check repository structure section matches reality

---

## 📝 Step 8: Verify `COMMANDS.md`

### Required Commands

Verify all these exist in `COMMANDS.md`:

- [ ] EXTRACT (conclusion, framework, checklist, narrative, metaphor) + RU aliases
- [ ] MARK (book_chapter, book_section, article, blog_post) + RU aliases
- [ ] ORGANIZE (knowledge blocks, themes, duplicates) + RU aliases
- [ ] ASSEMBLE (blog, article, book, email) + RU aliases
- [ ] SUGGEST (extract, organization, assembly) + RU aliases
- [ ] SET status (draft, solid, used, deprecated) + RU aliases
- [ ] SEARCH archive + RU aliases + behavior constraints

### Action Items

- [ ] Verify all commands from agent files exist in `COMMANDS.md`
- [ ] Verify Russian aliases are documented
- [ ] Verify SEARCH archive constraints are documented
- [ ] Ensure strict language: "must be exact, no freeform"

---

## 📝 Step 9: Move `pipeline.yaml`

### Current Location
- Root: `pipeline.yaml`

### Target Location
- `knowledge/pipelines/pipeline.yaml`

### Action Items

- [ ] Move `pipeline.yaml` to `knowledge/pipelines/pipeline.yaml`
- [ ] Update all references in:
  - `AGENTS.md`
  - `AGENTS/Assembler.md`
  - `README.md` (if mentioned)
  - Any documentation files

---

## 📝 Step 10: Update Documentation Files

### Files to Check

- `docs/User-Guide.md`
- `docs/Quick-Reference.md`
- `docs/Getting-Started.md`
- `docs/Cursor Workflow.md`
- `docs/index.md`

### Changes Required

1. **Pipeline Path**
   - Find: `pipeline.yaml`
   - Replace: `knowledge/pipelines/pipeline.yaml`

2. **Agent References**
   - Update to reflect new structure:
     - `AGENTS.md` → constitution
     - `AGENTS/Extractor.md` → specific agent
     - etc.

3. **Path References**
   - Verify all block paths use `knowledge/blocks/...`
   - Verify all source references use absolute paths

### Action Items

- [ ] Search all docs for `pipeline.yaml` → update to `knowledge/pipelines/pipeline.yaml`
- [ ] Search all docs for `blocks/...` → update to `knowledge/blocks/...`
- [ ] Update agent references if needed
- [ ] Verify consistency across all documentation

---

## ✅ Step 11: Final Verification Checklist

### Structure Checks

- [ ] `AGENTS.md` contains no "Extractor/Organizer/Assembler instructions"
- [ ] Each file in `AGENTS/*.md` contains a `## Command normalization` section
- [ ] `AGENTS/` directory exists with 4 files

### Path Checks

- [ ] Pipeline references use: `knowledge/pipelines/pipeline.yaml`
- [ ] Assembler Sources use: `knowledge/blocks/...`
- [ ] All relative paths replaced with absolute paths

### Command Checks

- [ ] Every command mentioned in agent files exists in `COMMANDS.md`
- [ ] No "extra commands" exist outside `COMMANDS.md`
- [ ] All Russian aliases documented in both `COMMANDS.md` and agent files

### File Checks

- [ ] `pipeline.yaml` moved to `knowledge/pipelines/pipeline.yaml`
- [ ] All references to `pipeline.yaml` updated
- [ ] `README.md` updated if needed
- [ ] Documentation files updated if needed

### Content Checks

- [ ] ArchiveSearch safety boundaries explicit
- [ ] Assembler path fixes applied
- [ ] Organizer rules in MUST/MUST NOT format
- [ ] SUGGEST never writes files (documented everywhere)

---

## 🚀 Step 12: Commit Plan

### Stage All Changes

```bash
git add AGENTS.md AGENTS/ COMMANDS.md knowledge/pipelines/pipeline.yaml README.md docs/ tools/ archive/ index/
```

### Commit Message

```
refactor: split agents, formalize commands, add archive search contract

- Split AGENTS.md into separate agent files (Extractor, Organizer, Assembler, ArchiveSearch)
- Make AGENTS.md constitution-only with global rules
- Add Command normalization sections to each agent file
- Fix Assembler source references to use knowledge/blocks/ paths
- Standardize pipeline path to knowledge/pipelines/pipeline.yaml
- Move pipeline.yaml to knowledge/pipelines/
- Update all path references across documentation
- Verify all commands documented in COMMANDS.md
```

---

## 📊 Summary

**Files to Create:** 4
- `AGENTS/Extractor.md`
- `AGENTS/Organizer.md`
- `AGENTS/Assembler.md`
- `AGENTS/ArchiveSearch.md`

**Files to Modify:** 3+
- `AGENTS.md` (major rewrite)
- `README.md` (path updates)
- Documentation files (path updates)

**Files to Move:** 1
- `pipeline.yaml` → `knowledge/pipelines/pipeline.yaml`

**Files to Verify:** 1
- `COMMANDS.md` (ensure all commands present)

**Total Changes:** ~10 files affected

---

## 🎯 Definition of Done

The refactoring is complete when:

- ✅ AGENTS are split into separate files
- ✅ AGENTS.md is constitution-only
- ✅ COMMANDS.md is the single command source of truth
- ✅ Assembler references correct block paths (`knowledge/blocks/...`)
- ✅ Pipeline path is consistent everywhere (`knowledge/pipelines/pipeline.yaml`)
- ✅ SEARCH archive is documented and constrained
- ✅ All documentation updated
- ✅ All paths use absolute references
- ✅ All commands verified in COMMANDS.md

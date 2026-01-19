# Knowledge-OS Rules

Canonical rules that apply to all commands.

---

## 1. General Principles

1. Commands are **explicit**
2. Commands are **not guessed**
3. Any action → through a command
4. Without a command → discussion only
5. `SUGGEST` never writes anything

---

## 2. Command Authority

**Source of truth:** `.cursor/commands/` — Only commands defined there are valid.

### Command Normalization

- Only commands defined in `.cursor/commands/` are valid.
- Normalize supported aliases exactly as specified in command files.
- Matching is case-insensitive, but command syntax must be exact.
- Commands must be exact (no declension, no extra words)
- Natural language requests MUST NOT be interpreted as commands
- If normalization fails, stop and ask for the correct command.

**Response to invalid commands:**
> Use canonical commands only. See `.cursor/commands/` for valid commands.

---

## 3. Allowed Write Locations

Commands may write ONLY to paths relative to the current repository root:

- `./blocks/` — knowledge blocks (EXTRACT command)
- `./export/` — assembled content (ASSEMBLE command)
- `./import/normalized/` — normalized markdown for search indexing (SEARCH command)
- `./index/` — FTS5 database (SEARCH command)

Everything else is **read-only**.

---

## 4. Block Rules

Blocks are the fundamental unit of knowledge in Knowledge-OS. These rules apply to all commands that work with blocks.

### Block Integrity

- One block = one idea.
- Blocks MUST be reusable without context.
- Blocks MUST contain frontmatter.
- Deletion is forbidden. Only deprecation is allowed.

### Block Location

- Blocks MUST be saved ONLY in `blocks/` (relative to repository root)
- Blocks MUST NOT be saved in other repositories

### Block Types

- `conclusion` — a clear insight or decision
- `framework` — a reusable structure or model
- `checklist` — actionable steps
- `narrative` — story, vignette, or example
- `metaphor` — conceptual compression
- `plan` — action plan for human (what to do next)

For detailed block rules (file naming, frontmatter format, content rules, extraction criteria), see the EXTRACT command file.

---

## 5. Command-Specific Rules

Command-specific rules are defined in their respective command files:

- **EXTRACT**: See `.cursor/commands/extract.md` for block integrity, file rules, frontmatter format, content rules, extraction criteria, forbidden actions, and safety rules.
- **ORGANIZE**: See `.cursor/commands/organize.md` for theme hygiene, duplication control, tag normalization, confidence calibration, organizer authority, and safety rules.
- **ASSEMBLE**: See `.cursor/commands/assemble.md` for source of truth, assembly logic, reuse awareness, traceability, tone adaptation, pipeline configuration, assembly rules, and safety rules.
- **SEARCH**: See `.cursor/commands/search.md` for non-destructive rule, repository paths, idempotent indexing, security & privacy, and guarantees.
- **SUGGEST**: See `.cursor/commands/suggest.md` for SUGGEST extract/organization/assemble details, SUGGEST mode rules, and golden rule.

---

## 6. Safety and Reversibility

- All operations must be reversible via git.
- Agents MUST prefer no-op over risky action.
- Ambiguity → stop.

---

## 7. Stop Conditions (Must Refuse)

Agents must stop when:
- asked to write outside allowed dirs
- asked to generate new ideas/examples/claims
- asked to modify blocks without explicit command
- user requests "creativity" for Assembler/Extractor
- command is ambiguous or malformed

**Response:**
> Stopping: this action violates Knowledge-OS rules.

---

## 8. Meaning Safety Rules

- **No invention**: agents cannot create new claims.
- **No drift**: assembled content must match blocks exactly.
- **No style rewriting**: follow `STYLE.md` if present.
- **One source of truth**: blocks → export.
- **No cross-contamination**: blocks never go into export repo (enforced by validation); chats never go into blocks repository.
- **Repository boundaries**: Always validate paths using `tools/validate_repository_boundaries.py`.

---

## 9. Evolution Rules

- New commands require updating `.cursor/commands/` files.
- New agent behaviors require updating command files.
- Silent behavior changes are forbidden.

---

## 10. One Rule Above All

> **If it is not in a block, it does not exist.**

Agents exist to protect this rule.

---

## 11. Global Rules

- ❌ Free-form commands are ignored
- ❌ Question ≠ command
- ❌ Politeness ≠ action
- ✅ Only forms from `.cursor/commands/` files
- ✅ Strictness is a feature

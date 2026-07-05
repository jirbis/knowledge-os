---
id: P1-002
type: P1            # standard changes; individual items marked P0 where they are pure clarification
status: proposed
date: 2026-07-05
title: Document consistency — one taxonomy, one schema source, no dead references
relates_to:
  - .cursor/rules.md
  - .cursor/commands/
  - config.yaml
  - README.md
  - CLAUDE.md
  - tools/init_repository.py
  - .gitignore
---

# P1-002 — Document consistency

## Summary

The canon contradicts itself in mechanically checkable ways: the block-type taxonomy
differs across four files, cross-references point to sections that do not exist, the
frontmatter schema lives in the wrong document, ASSEMBLE's pipeline configuration is
duplicated outside `config.yaml`, and dead functionality (STATUS, the Telegram ingest
path) violates OCCAM-4 ("deletion is default"). Silent drift between documents is
exactly what §9 "Evolution Rules" forbids. This proposal aligns all documents to a
single source of truth. It adds no new moving parts.

## Findings and changes

### F1. Block-type taxonomy diverges in four places (P1)

| Source | Types |
|---|---|
| `.cursor/rules.md` §4 | conclusion, framework, checklist, narrative, **metaphor**, plan |
| `config.yaml` `block_types` | frameworks, checklists, plans, narratives, conclusions, **patterns** |
| `README.md` | framework, checklist, conclusion, narrative, plan, **pattern** |
| `tools/init_repository.py` | creates `blocks/metaphors`, **no** `blocks/patterns` |

**Change:** declare the canonical list once, in `config.yaml`, and make every other
document reference it. Proposed canonical set (owner confirms membership):
`conclusion, framework, checklist, narrative, metaphor, plan, pattern`.
Update `rules.md` §4, `extract.md`, README, `init_repository.py` accordingly.

### F2. Broken cross-references (P0)

- Every command file ends with "See `.cursor/rules.md` §10-12, §15" — rules.md has
  §1–§11. Point to real sections.
- `rules.md` §4 says the frontmatter format is in the EXTRACT command file — it is
  not (it exists only in CLAUDE.md). Move the schema into `extract.md` (or a schema
  file referenced from `config.yaml`) so the promise holds.
- `search.md` cites "rules.md §8 for idempotent indexing" — §8 is Meaning Safety.

### F3. Two sources of configuration truth (P1)

ASSEMBLE's pipeline rules (`min_confidence`, `tone`, `reuse_must_include`) are a YAML
block hard-coded inside `assemble.md`, violating the system's own OCCAM-2
("configuration over code"). Move them into `config.yaml` under `pipeline.targets`;
`assemble.md` references them.

Also: `config.yaml` `allowed_output_paths` lists only `./export`, while rules §3
allows `./import/normalized/` and `./index/` too. Align config to rules (this is also
a precondition for the allowlist enforcement in P2-001).

### F4. ORGANIZE contradicts the EXTRACT-only rule (P1)

`organize.md` permits "non-destructive edits when explicitly confirmed"; CLAUDE.md
forbids modifying blocks without EXTRACT; `config.yaml` marks blocks protected.
**Change:** define an explicit `ORGANIZE apply` sub-command with a documented
confirmation protocol (proposal listed → user confirms by number → metadata-only edit),
and name it in rules §3 as the sole non-EXTRACT path that may touch block frontmatter.
(Enforced via `--intent organize --confirmed` in the P2-001 validator.)

### F5. Dead functionality — OCCAM-4 (P1)

- `status.md` says of itself "Candidates are deprecated. This command may be removed."
  Remove the command file (and its row in README/CLAUDE.md tables), or implement
  candidates for real. Recommendation: remove.
- `search.md` instructs agents to run `tools/ingest_telegram_export.py` "(to be
  created)" — the file does not exist, so the Telegram path of SEARCH fails.
  Remove the Telegram branch from the command, or write the tool.
  Recommendation: remove until needed.
- README says "See repository for license details" — there is no LICENSE file.
  Add one (owner picks the license).

### F6. `.gitignore` hygiene (P0)

Duplicate and conflicting entries: `blocks` listed twice, both `export` and `export/`;
`!index/.keep` and `!import/.keep` negations exist but the `.keep` files themselves do
not, so `index/` and `import/` vanish in a fresh clone and the README's repository
structure diagram is wrong. Deduplicate, and add the missing `.keep` files (final
content of this file depends on the P2-001 C6 decision about tracking `blocks/`).

### F7. CLAUDE.md describes a repository that does not exist (P1)

CLAUDE.md (v1.0, dated 2026-02-13) references ~10 files under `blocks/frameworks/` and
`blocks/checklists/` that are absent from the repository, presents STATUS as active,
and restates schemas that exist nowhere else. Regenerate CLAUDE.md from the actual
repository state after F1–F6 land, and keep it a *pointer* document: it should
reference canon files, not restate their content (restatement is how the current drift
happened).

### F8. Command-language consistency (P0)

`help.md` defines Russian aliases (ПОМОЩЬ, СПРАВКА), while `search.md`'s workflow
example uses `ИЗВЛЕЧЬ вывод / чеклист / фреймворк` — a command defined nowhere,
despite rules §2 requiring exact-match normalization from command files only.
Either define Russian aliases per command in the command files, or use canonical
English commands in all examples. Recommendation: canonical English in examples;
aliases only where explicitly defined.

## Occam note

No new moving parts. Net effect is negative complexity: one command file removed,
one phantom tool reference removed, one configuration source instead of two.

## Reversal plan

Pure documentation/configuration edits; revert via git.

## Acceptance criteria

- [ ] `grep -r "§1[2-5]" .cursor/` returns nothing; all section references resolve.
- [ ] Block-type list appears in exactly one file (`config.yaml`); all others reference it.
- [ ] Frontmatter schema lives where `rules.md` §4 says it lives.
- [ ] ASSEMBLE pipeline table exists only in `config.yaml`.
- [ ] `allowed_output_paths` matches rules §3 exactly.
- [ ] No document references `status.md`, `ingest_telegram_export.py`, or missing block files.
- [ ] LICENSE file exists.
- [ ] Fresh clone contains every directory shown in README's structure diagram.

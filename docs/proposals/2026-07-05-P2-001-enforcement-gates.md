---
id: P2-001
type: P2            # complexity increase — Occam Test required
status: proposed
date: 2026-07-05
title: Make enforcement real — boundary validator, CHECK, CI, harness guardrails
relates_to:
  - tools/validate_repository_boundaries.py
  - config.yaml
  - .cursor/rules.md
  - .gitignore
---

# P2-001 — Make enforcement real

## Summary

Knowledge-OS declares itself a *constitutional* repository: rules are supposed to be
enforced, not merely stated. Today every safety guarantee exists only as prompt text.
The single technical gate — `tools/validate_repository_boundaries.py` — contradicts the
constitution it is meant to protect, and the source of truth (`blocks/`) is excluded
from git, making "reversible via git" and "deletion is forbidden" unenforceable.

This proposal closes the gap between declaration and enforcement.

## Motivation — observed defects (with evidence)

### D1. The boundary validator blocks legitimate EXTRACT

`config.yaml` marks `./blocks` as protected, while `.cursor/rules.md` §3 allows the
EXTRACT command to write there. CLAUDE.md's "Write Operation Safety Protocol" requires
running the validator before **any** write. Reproduced:

```
$ python3 tools/validate_repository_boundaries.py --check-path ./blocks/conclusions/new-block.md
ERROR: Write operation forbidden: ./blocks/conclusions/new-block.md
exit=1
```

A compliant agent can therefore never extract a block.

### D2. The validator does not enforce the allowlist

It only answers "is this path protected?", never "is this path allowed?". Writing to
the constitution itself passes:

```
$ python3 tools/validate_repository_boundaries.py --check-path ./.cursor/rules.md
OK: All validations passed
exit=0
```

### D3. The validator fails open when run outside the repo root

`get_protected_paths()` builds `repo_root / Path(p).resolve()` — `resolve()` on a
relative path resolves against the *current working directory*, and `repo_root` is
`Path.cwd()`. Run from any other directory, every check passes:

```
$ cd /home/user && python3 knowledge-os/tools/validate_repository_boundaries.py \
    --check-path /home/user/knowledge-os/blocks
OK: All validations passed
exit=0
```

### D4. The source of truth is not versioned

`.gitignore` excludes `blocks`, `export`, `index`, `import`. Consequences:

- `.cursor/rules.md` §6 "All operations must be reversible via git" — impossible;
  git does not track blocks.
- §4 "Deletion is forbidden" — unenforceable and undetectable.
- CLAUDE.md references many `blocks/frameworks/*.md` and `blocks/checklists/*.md`
  documents that do not exist in a fresh clone; the constitution cites documents
  that are not there.

### D5. CHECK protocol is declared but not implemented

CHECK is described as a "constitutional barrier" producing `check_report.md`, yet no
check script, no CI (`.github/` absent), and no pre-commit hooks exist. Additionally,
the repo root — where `check_report.md` must be written — is not an allowed write path,
and neither is any location for proposal artifacts.

### D6. Prompt-only enforcement is vulnerable to prompt injection

EXTRACT and SEARCH process untrusted content (chat exports). All write restrictions
live in prompt text; nothing at the filesystem or harness level prevents an injected
instruction from writing anywhere.

## Proposed changes

### C1. Rewrite `tools/validate_repository_boundaries.py`

- Enforce the **allowlist** from `.cursor/rules.md` §3: writes permitted only under
  `./blocks/`, `./export/`, `./import/normalized/`, `./index/`,
  `./docs/proposals/`, and `./check_report.md` (see C4). Everything else fails.
- Add `--intent extract|assemble|search|organize|check`:
  - `extract` → `blocks/` writable, everything else read-only;
  - `assemble` → `export/` writable;
  - `search` → `import/normalized/` and `index/` writable;
  - `organize` → `blocks/` metadata-writable only with `--confirmed` flag;
  - `check` → `check_report.md` writable.
  This resolves the D1 contradiction: `blocks/` stays protected *from the pipeline*
  (ASSEMBLE/SEARCH) while remaining writable *for EXTRACT*.
- Detect repo root via `git rev-parse --show-toplevel` (fallback: directory containing
  `config.yaml`), never via bare CWD. Fail **closed**: unresolvable root, missing or
  unparseable config → exit 1.
- Unit tests covering D1–D3 regressions.

### C2. Implement CHECK as code — `tools/check.py`

A single deterministic script that validates and writes `check_report.md`:

1. Block frontmatter conforms to schema (type, themes, confidence, reuse, source, tags).
2. Block filenames follow naming rules; deprecated blocks carry the deprecation marker.
3. No deleted files under `blocks/` (`git diff --diff-filter=D` against the merge base).
4. Cross-references between `.cursor/rules.md`, command files, README, CLAUDE.md
   resolve (no dangling section numbers or missing files).
5. Boundary validator self-test passes.

Exit 0 = CHECK PASS, exit 1 = CHECK FAIL. No task is done without PASS.

### C3. CI + pre-commit

- `.github/workflows/check.yml`: run `tools/check.py` and the validator test suite on
  every push and PR.
- `.pre-commit-config.yaml`: the same checks locally before commit.

### C4. Legalize artifact locations

Amend `.cursor/rules.md` §3 and `config.yaml` to add two allowed write locations:
`./docs/proposals/` (proposal artifacts — required by the proposal mechanism) and
`./check_report.md` (required by CHECK). Without this, the constitution's own
mechanisms violate the constitution.

### C5. Harness-level guardrails

Add `.claude/settings.json` (shared via the existing `.claude -> .cursor` symlink
pattern) with `permissions.deny` rules forbidding Write/Edit outside allowed paths,
plus a `PreToolUse` hook invoking the validator. Rules then hold even against prompt
injection from ingested chat exports, independent of model obedience.

### C6. Decision point — versioning of `blocks/` (owner must choose)

- **Option B (recommended): track `blocks/` in git.** Remove it from `.gitignore`.
  "Reversible via git", "deletion forbidden", and CHECK's deletion guard become real.
  If the repository must stay public while blocks are private, make this repo private
  or move blocks to a private submodule.
- **Option A: keep blocks untracked, state it honestly.** Rewrite rules §6 to name the
  actual backup mechanism, remove the git-reversibility claim, and delete CLAUDE.md
  references to non-existent block files. CHECK items 1–3 then run only locally.

Everything else in this proposal is valid under either option, but Option A leaves
"deletion is forbidden" permanently unenforceable in CI.

## Occam Test (required for P2)

| New moving part | Necessity proof |
|---|---|
| Rewritten validator | The current one is provably wrong (D1–D3); not adding a part, fixing one. |
| `tools/check.py` | CHECK is already mandated by the constitution; this is the missing implementation, not a new concept. |
| One CI workflow | Only mechanism that makes rules hold for every contributor and agent; a single YAML file. |
| Pre-commit config | Same checks, earlier; one declarative file, no new logic. |
| `.claude/settings.json` deny rules | Only defense that does not depend on model obedience (D6); declarative, no code. |

**Not added, deliberately:** no server, no database, no new command, no external
service, no framework. All checks are stdlib Python + git. Configuration over code
(OCCAM-2): allowed paths continue to live in `config.yaml`.

## Complexity budget

- 1 rewritten tool, 1 new tool (~200 lines), 2 declarative config files,
  1 CI workflow, 1 test module. No new runtime dependencies (pyyaml already required).

## Reversal plan

Delete `.github/workflows/check.yml`, `.pre-commit-config.yaml`,
`tools/check.py`, `.claude/settings.json`; revert the validator and
`config.yaml`/rules edits via git. No data migration in either direction.

## Acceptance criteria (CHECK PASS conditions)

- [ ] `--check-path ./blocks/... --intent extract` passes; `--intent assemble` fails.
- [ ] `--check-path ./.cursor/rules.md` fails for every intent.
- [ ] Validator run from any CWD produces identical results.
- [ ] `tools/check.py` produces deterministic `check_report.md`; CI runs it on PRs.
- [ ] Deleting a file under `blocks/` fails CHECK (under Option B).
- [ ] Owner has recorded a decision on C6 in this proposal's status.

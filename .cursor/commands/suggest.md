# SUGGEST — suggest (NO write)

Never creates files.  
Used when uncertain.

## Canonical commands

```
SUGGEST extract
SUGGEST organization
SUGGEST assemble
```


## Effect

- form proposals
- structure proposals
- confirmation request



## SUGGEST extract

**What Extractor can suggest:**

- block type (conclusion / checklist / framework / narrative / metaphor / plan)
- tentative filename
- primary theme
- confidence level

**Output format:**

Suggestions MUST be listed explicitly, for example:

```
Suggested extractions:
1. conclusion — "workflow-tools-vs-ai-protocols"
2. framework — "executable-protocols"
3. checklist — "when-to-replace-workflow-tool"
```




**Follow-up:**

Extractor MUST ask: "Select items to EXTRACT (e.g. `1`, `1,3`, `2-4`, or `all`)?"

Allowed answers:
- `<numbers>` — Extract the selected items (one-by-one, in listed order), e.g. `1`, `1,3`, `2-4`.
- `all` — Extract **all suggested blocks** (one-by-one, in the listed order).
- `none` — Do nothing (no files created).

Rules for selection / `all` (MUST):
- Extractor MUST create one file per selected item (still: one block → one file).
- Extractor MUST use the suggested **type** and **tentative filename** (slug) for each item.
- Extractor MUST preserve the suggested order (numerical order), even if the user types `3,1`.
- If any selected item is missing required info (type/filename/theme) → stop and ask **before writing anything**.
- If the selection is malformed or references out-of-range items → ask for clarification (no writes).

## SUGGEST organization

**What Organizer can suggest:**

- potential duplicates
- theme misalignment
- possible merges
- candidate promotion or deprecation

**Output format:**

Suggestions MUST be non-destructive and include rationale.

## SUGGEST assemble

**What Assembler can suggest:**

- content type (blog / article / book / email / diary)
- suitable candidates
- missing blocks
- best pipeline

**Output format:**

Suggestions MUST include:
- proposed output
- required blocks
- estimated completeness (low/medium/high)

Assembler MUST NOT assemble in SUGGEST mode.

## SUGGEST Mode Rules

SUGGEST is an advisory mode.  
It MUST NOT create or modify any files.

**SUGGEST may:**
- analyze the current context
- propose block types
- suggest titles and themes

**SUGGEST must:**
- clearly label suggestions as non-persistent
- ask for explicit confirmation before any EXTRACT or ASSEMBLE

If user does not confirm, nothing is written.

## Golden Rule

> **When uncertain → SUGGEST  
> When decided → EXTRACT / ASSEMBLE**

If a command is not written — nothing happens.

See `.cursor/rules.md` for:
- General principles (§1)
- Command normalization (§2)
- Global safety rules (§10-12)
- Global rules (§15)

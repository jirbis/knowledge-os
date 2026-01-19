# SET status — candidate state management

## Canonical commands

```
SET status: draft
SET status: solid
SET status: used
SET status: deprecated
```


## Candidate lifecycle

Candidates have lifecycle states:
- `draft` — initial state
- `solid` — ready for use
- `used` — has been assembled into export
- `deprecated` — no longer used (but preserved)

**Note:** Candidates are deprecated. This command may be removed in future versions.

See `.cursor/rules.md` for:
- General principles (§1)
- Global rules (§15)

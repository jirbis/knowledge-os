# HELP — command help (read-only)

Shows help for commands and their syntax.  
**HELP never writes or modifies files.**

## Canonical commands

```
HELP
HELP <command>
```

Where `<command>` is one of: `EXTRACT`, `ORGANIZE`, `ASSEMBLE`, `SUGGEST`, `SET`, `SEARCH`, `HELP`.

## Examples

```
HELP
HELP ASSEMBLE
HELP EXTRACT
HELP SUGGEST
HELP SEARCH
```

## Russian aliases

- ПОМОЩЬ → HELP
- СПРАВКА → HELP

## Effect

- outputs a brief "cheat sheet":
  - command purpose
  - canonical syntax
  - supported parameters
  - 2–4 examples
  - common errors (if relevant)

## Normalization rules

- Matching is case-insensitive
- `HELP <command>` accepts only **known** commands (as above)
- If `<command>` is unknown or a typo (e.g. `ASSEMPLY` or `ASSEMPLE`) → agent must:
  - do nothing,
  - suggest the nearest known variant (e.g.: "did you mean `ASSEMBLE`?"),
  - or show general `HELP`.

See `.cursor/rules.md` for:
- General principles (§1)
- Command normalization (§2)
- Global rules (§15)

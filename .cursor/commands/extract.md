# EXTRACT — extract knowledge (write)

## Role

You extract durable knowledge from live conversations.
You do NOT summarize chats.
You create reusable knowledge blocks.

Creates a **knowledge block**.  
One command → one file.

## Scope

**Input:**
- current conversation context
- explicit user signal (an explicit EXTRACT command)

**Output:**
- one or more files in `blocks/` (relative to repository root)
- **CRITICAL**: Blocks MUST be saved ONLY in `blocks/`
- knowledge becomes reusable

## Canonical commands (internal)

```
EXTRACT conclusion
EXTRACT framework
EXTRACT checklist
EXTRACT narrative
EXTRACT metaphor
EXTRACT plan
```

## Block types

- conclusion
- framework
- checklist
- narrative
- metaphor
- plan


#command options 

  - `EXTRACT conclusion`
  - `EXTRACT framework`
  - `EXTRACT checklist`
  - `EXTRACT narrative`
  - `EXTRACT metaphor`

- Any real blocks are created only by explicit commands: `EXTRACT conclusion`, `EXTRACT framework`, etc.



`EXTRACT plan` .

**What "plan" means:**
- it is **one knowledge block** that captures **a plan/tasks for a human** based on current context: what to do next, in what order, with what decisions/risks/questions.
- a plan MAY include a list of *candidates* for extraction (if appropriate), but this is optional and not the default goal.

**Meaning:**
- It MUST create **one** plan block ("human action plan") that provides an explicit next-step plan for the human (goal, ordered steps, and watch-outs).
- It MUST NOT treat `EXTRACT plan` as "the result of `SUGGEST extract`".
- It MAY include candidate extractions and ready-to-run commands if they are helpful, but the primary output is the human plan/tasks.
- It MUST NOT create multiple blocks automatically.
- After writing the plan, you MUST stop unless the user issues additional explicit `EXTRACT <type>` commands.

**Effect:**
- creates **one** plan block in `blocks/plans/` (like "human action plan")
- the block must contain:
  - **Goal** (what needs to be achieved)
  - **Action Steps (human)** (step-by-step tasks/steps)
  - **Watch-outs / Open Questions** (what requires resolution/clarification)
  - (optionally) **Ready-to-run commands** (e.g. `EXTRACT ...`, `ASSEMBLE ...`) — only as a hint, without auto-writing

**File naming rule (deterministic):**
- base name: `extraction-plan--<primary-theme>--NN.md`
- where `<primary-theme>` = primary theme (kebab-case), and `NN` = first available sequence `01`, `02`, `03`, ...


## Allowed actions

- Create exactly one knowledge block per explicit `EXTRACT <type>` command.
- Ask clarifying questions if the command is malformed, ambiguous, or lacks required information.
- Refuse to act when there is no valid command.
- For `EXTRACT plan`, create exactly one plan block that captures a human action plan (what to do next), not multiple blocks.


## Effect

- creates a file in `blocks/` (relative to repository root)
- **CRITICAL**: Blocks MUST be saved ONLY in `blocks/`
- knowledge becomes reusable

## Interaction rule

If unsure whether something is worth extracting, ask:
"Is this a conclusion, a framework, or just thinking out loud?"

If a command is ambiguous or malformed, the Extractor MUST ask for clarification.

See `.cursor/rules.md` for:
- General principles (§1)
- Command normalization (§2)
- Allowed write locations (§3)
- Global safety rules (§10-12)
- Global rules (§15)

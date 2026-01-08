---
type: checklist
themes:
  - knowledge-os
  - automation
confidence: high
reuse:
  - blog
  - book
  - consulting
source: chat
tags:
  - checklist
  - repository
  - cursor
  - agents
  - workflow
---

# Repository Readiness Checklist — Knowledge OS

## Basic Structure
- README.md exists
- AGENTS.md exists
- COMMANDS.md exists
- `knowledge/` directory created
- `knowledge/` contains: blocks / candidates / pipelines

## Agents
- AGENTS/Extractor.md exists
- AGENTS/Organizer.md exists
- AGENTS/Assembler.md exists
- Each agent has `Command normalization` section
- Each agent describes `SUGGEST` mode

## Command Discipline
- All commands defined in COMMANDS.md
- Russian aliases documented
- No "hidden" or verbal commands
- Conversational speech does not trigger actions

## Knowledge Blocks
- 1 file = 1 idea
- No dates in filenames
- Frontmatter present
- Type specified
- At least 1 theme specified
- Reuse specified
- Block is readable without context

## Content Candidates
- `knowledge/candidates/` directory exists
- At least one candidate exists
- Candidate does not duplicate blocks
- Status present
- source_blocks present
- Clear what candidate can become (chapter / article / post)

## Pipelines
- `knowledge/pipelines/pipeline.yaml` exists
- blog / book / email described
- min_confidence specified
- reuse_must_include specified
- Assembler constrained by pipeline rules

## Output
- `output/` directory exists
- Output is not edited manually
- Output contains Sources section
- Sources point to blocks / candidates

## SUGGEST Mode
- `SUGGEST extract` does not create files
- `SUGGEST assembly` does not create output
- Explicit confirmation required after SUGGEST
- Nothing happens without a command

## Git and Reversibility
- Repository under git
- Commits are small and meaningful
- Any action can be reverted
- No changes without commit

## Final Test
- Clear what ideas exist
- Clear which are candidates
- Visible what has been used
- Can quickly assemble content without regenerating

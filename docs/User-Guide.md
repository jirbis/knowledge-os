# User Guide: Knowledge Operating System (KOS)

Complete guide to using KOS for extracting, organizing, and reusing knowledge from conversations.

## Table of Contents

1. [Understanding KOS](#understanding-kos)
2. [Repository Structure](#repository-structure)
3. [Working with Knowledge Blocks](#working-with-knowledge-blocks)
4. [Using Agents](#using-agents)
5. [Content Candidates](#content-candidates)
6. [Pipelines](#pipelines)
7. [Daily Workflow](#daily-workflow)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Understanding KOS

### Core Philosophy

KOS is built on five principles:

1. **Chats are raw material** — Conversations are ephemeral thinking space
2. **Blocks are truth** — Only extracted blocks are durable knowledge
3. **Candidates are intent** — Potential content structures, not prose
4. **Outputs are assemblies** — Content is built from blocks, not written from scratch
5. **Nothing valuable lives only in chat history** — Extract or lose it

### Mental Model

- **Chat** → thinking space (ephemeral)
- **Extractor** → turns thinking into blocks
- **Organizer** → maintains order and coherence
- **Candidates** → potential chapters, articles, posts
- **Assembler** → builds content from blocks
- **Git** → long-term memory

You don't "write content." You **build a knowledge system that produces content**.

---

## Repository Structure

```
knowledge/
  blocks/              # Atomic, reusable knowledge (source of truth)
    conclusions/       # Clear insights or decisions
    frameworks/        # Reusable structures or models
    checklists/        # Actionable steps
    narratives/        # Stories, vignettes, examples
    metaphors/         # Conceptual compression
  
  candidates/          # Potential content units (structure, not prose)
    book/
    chapters/
    sections/
    articles/
    posts/
  
  pipelines/           # Routing rules (what goes where)
    pipeline.yaml
  
  themes/              # Theme definitions (stable concepts)
    ai-agents.md
    jira-decline.md
    health-parasites.md

AGENTS.md              # Agent instructions

output/                # Generated content (never edited manually)
  blog/
  book/
  email/
  diary/
```

---

## Working with Knowledge Blocks

### Block Rules

- **One idea per file** — Never merge unrelated ideas
- **No dates in filenames** — Use semantic names
- **No project-specific naming** — Blocks should be reusable
- **Written for blind reuse** — Another agent should understand it without context

### Block Types

#### Conclusion
A clear insight or decision. Example:
```yaml
type: conclusion
themes: [ai-agents]
confidence: high
reuse: [blog, book, email]
tags: [ai, agents]
---
AI agents work best when given executable protocols, not just descriptions.
```

#### Framework
A reusable structure or model. Example:
```yaml
type: framework
themes: [executable-protocols]
confidence: medium
reuse: [blog, book]
tags: [protocols, structure]
---
# Protocol Structure
1. Trigger condition
2. Required inputs
3. Execution steps
4. Success criteria
```

#### Checklist
Actionable steps. Example:
```yaml
type: checklist
themes: [knowledge-extraction]
confidence: high
reuse: [blog, email]
tags: [extraction, workflow]
---
- [ ] Identify valuable insight
- [ ] Determine block type
- [ ] Create semantic filename
- [ ] Add frontmatter
- [ ] Write content
```

#### Narrative
Story, vignette, or example. Example:
```yaml
type: narrative
themes: [jira-decline]
confidence: medium
reuse: [blog, book]
tags: [jira, workflow]
---
The team spent three hours configuring Jira workflows for a task that took 15 minutes to complete.
```

#### Metaphor
Conceptual compression. Example:
```yaml
type: metaphor
themes: [knowledge-management]
confidence: high
reuse: [blog, book]
tags: [metaphor, thinking]
---
Knowledge blocks are like LEGO bricks: atomic, reusable, composable.
```

### Block Frontmatter

Every block must include frontmatter:

```yaml
type: <conclusion|framework|checklist|narrative|metaphor>
themes:
  - <primary-theme>
  - <optional-secondary-theme>
confidence: <low|medium|high>
reuse:
  - blog
  - book
  - email
source: chat
tags:
  - canonical-tag-1
  - canonical-tag-2
```

**Field descriptions:**

- `type`: Block type (required)
- `themes`: Stable concepts, not projects (1-2 max)
- `confidence`: How certain you are about this knowledge
- `reuse`: Where this block can be used
- `source`: Origin (usually "chat")
- `tags`: Canonical tags for discovery (max 10)

### Naming Conventions

- Use **kebab-case**: `jira-workflows-vs-ai-protocols.md`
- Be **semantic**: Describe the idea, not the date
- Avoid **project names**: `client-x-insight.md` → `workflow-automation-pattern.md`

---

## Using Agents

### Extractor Agent

**Purpose:** Extract durable knowledge from conversations.

**When to use:**
- During or after a conversation
- When you spot valuable insight
- When you say "this is important"

**How to trigger:**
```
EXTRACT conclusion
EXTRACT framework
EXTRACT checklist
EXTRACT narrative
EXTRACT metaphor
```

**Russian aliases:**
- ИЗВЛЕЧЬ вывод → EXTRACT conclusion
- ИЗВЛЕЧЬ фреймворк → EXTRACT framework
- ИЗВЛЕЧЬ чеклист → EXTRACT checklist

**What it does:**
- Evaluates if extraction is warranted
- Chooses appropriate block type
- Creates file in `knowledge/blocks/`
- Adds proper frontmatter

**What it doesn't do:**
- Summarize entire chats
- Improve writing style
- Decide where content will go

### Organizer Agent

**Purpose:** Maintain coherence and prevent duplication.

**When to use:**
- Periodically (weekly/monthly)
- When you notice duplication
- When themes become messy
- On explicit request: `ORGANIZE knowledge blocks`

**How to trigger:**
```
ORGANIZE knowledge blocks
ORGANIZE themes
ORGANIZE duplicates
```

**Russian aliases:**
- ОРГАНИЗОВАТЬ блоки → ORGANIZE knowledge blocks
- ОРГАНИЗОВАТЬ темы → ORGANIZE themes
- ОРГАНИЗОВАТЬ дубликаты → ORGANIZE duplicates

**What it does:**
- Checks theme consistency
- Normalizes tags
- Identifies duplicates
- Proposes merges
- Updates metadata

**What it doesn't do:**
- Delete files (only deprecates)
- Rewrite content
- Invent new themes

**Deprecation example:**
```markdown
> ⚠️ Deprecated: merged into `knowledge/blocks/conclusions/unified-workflow-principle.md`
```

### Assembler Agent

**Purpose:** Build content from existing blocks.

**When to use:**
- When you need a blog post, chapter, email, etc.
- Never for generating new ideas

**How to trigger:**
```
ASSEMBLE blog
theme: ai-agents
length: medium

ASSEMBLE article
themes: ai-agents, executable-protocols
tone: deep

ASSEMBLE book
theme: health-parasites
length: long

ASSEMBLE email
theme: health-parasites
length: short
```

**Russian aliases:**
- СОБРАТЬ пост → ASSEMBLE blog
- СОБРАТЬ статью → ASSEMBLE article
- СОБРАТЬ книгу → ASSEMBLE book
- СОБРАТЬ письмо → ASSEMBLE email

**What it does:**
- Finds relevant blocks
- Checks `reuse` permissions
- Assembles content
- Adds source references
- Adapts tone (blog/book/email)

**What it doesn't do:**
- Generate new ideas
- Use content outside blocks
- Override block content

**Output format:**
```markdown
# Assembled Content

[Content assembled from blocks...]

---
Sources:
- blocks/conclusions/ai-agents-executable-protocols.md
- blocks/frameworks/protocol-structure.md
---
```

### ArchiveSearch Agent

**Purpose:** Search past conversations from ChatGPT or Telegram exports without creating knowledge blocks.

**When to use:**
- When you remember discussing something but can't find it
- Before extracting to avoid duplicating existing knowledge
- When you need context from past conversations

**How to trigger:**

**For ChatGPT:**
```
SEARCH archive export_path=/path/to/conversations.json query="search terms" limit=20
```

**For Telegram:**
```
SEARCH archive export_path=/path/to/telegram_export.json source_type=telegram query="search terms" limit=20
```

**Parameters:**
- `export_path`: Path to export file (ChatGPT `conversations.json` or Telegram export) (required on first run)
- `query`: FTS5 search query (required)
- `source_type`: Export source type - `chatgpt` or `telegram` (optional, auto-detected if not specified)
- `limit`: Number of results (optional, default 20)
- `reindex`: Force reindexing (optional, default false)

**Russian aliases:**
- ПОИСК архив → SEARCH archive
- НАЙТИ в архиве → SEARCH archive

**What it does:**
- Automatically indexes ChatGPT or Telegram exports if needed
- Detects export source type automatically (or uses `source_type` parameter)
- Performs full-text search using FTS5 across all indexed sources
- Returns ranked results with conversation IDs and snippets
- Provides next-step commands for extraction

**What it doesn't do:**
- Create or modify knowledge blocks
- Write to `knowledge/blocks/` or `knowledge/candidates/`
- Execute EXTRACT automatically

**Typical workflow:**
1. Search: `SEARCH archive query="jira workflows"`
2. Review results and select conversation
3. Extract snippet: `python3 tools/extract_snippet.py --id <conversation_id>`
4. Suggest extraction: `SUGGEST extract`
5. Extract if confirmed: `ИЗВЛЕЧЬ вывод` / `ИЗВЛЕЧЬ чеклист` / etc.

**FTS5 Query Tips:**
- **Exact phrase:** `"executable protocols"`
- **Boolean:** `jira OR confluence`
- **Proximity:** `jira NEAR/5 workflow`
- **Exclude:** `jira NOT datacenter`

**Allowed paths:**
- Creates/updates: `index/chats.sqlite`, `archive/normalized/*`
- Never touches: `knowledge/blocks/`, `knowledge/candidates/`, `output/`

### SUGGEST Agent (Advisory Mode)

**Purpose:** Propose actions without creating files.

**When to use:**
- When unsure what to extract
- When uncertain about organization needs
- When exploring assembly possibilities

**How to trigger:**
```
SUGGEST extract
SUGGEST organization
SUGGEST assembly
```

**What it does:**
- Analyzes context
- Proposes block types, themes, filenames
- Suggests organization improvements
- Recommends assembly strategies
- **Never creates files** — only suggests

**What it doesn't do:**
- Create or modify files
- Execute actions without confirmation

---

## Content Candidates

Candidates represent **potential content**, not finished text.

### Candidate Types

- `book_chapter` — Full chapter structure
- `book_section` — Section within chapter
- `article` — Long-form article
- `blog_post` — Blog post

### Candidate Properties

Candidates:
- Reference existing blocks
- Define structure and intent
- Evolve via status changes

### Candidate Lifecycle

```
draft → solid → used → deprecated
```

**Status meanings:**

- `draft`: Initial idea, structure forming
- `solid`: Structure complete, ready for assembly
- `used`: Already assembled into output
- `deprecated`: No longer relevant

**Managing candidate status:**

```
SET status: draft
SET status: solid
SET status: used
SET status: deprecated
```

**Creating candidates:**

```
MARK as book_chapter candidate
MARK as book_section candidate
MARK as article candidate
MARK as blog_post candidate
```

**Important:** Nothing is deleted. History matters.

---

## Pipelines

Pipelines define **where blocks are allowed to go**.

### Pipeline Examples

- **Blog** → public, medium confidence
- **Book** → deep, high confidence only
- **Email** → short, compressed
- **Diary** → private, unrestricted

### Pipeline Rules

Pipelines:
- Never generate ideas
- Never override blocks
- Only assemble

### Pipeline Configuration

Define pipelines in `knowledge/pipelines/pipeline.yaml`:

```yaml
blog:
  confidence: [medium, high]
  tone: public
  length: medium

book:
  confidence: [high]
  tone: deep
  length: long

email:
  confidence: [low, medium, high]
  tone: direct
  length: short
```

---

## Daily Workflow

### Typical Session

1. **Think in chat** — Discuss, explore, debate
2. **Spot value** — Recognize valuable insight
3. **EXTRACT** → Create block immediately
4. **Periodically ORGANIZE** — Weekly/monthly maintenance
5. **When needed: ASSEMBLE** → Build output

### Daily Micro-Ritual (10-15 minutes)

At the end of each day:

1. Check `git status`
2. Review new blocks
3. Quick cleanup:
   - Rename if needed
   - Adjust confidence
   - Update tags
4. Commit: `git commit -m "Extracted conclusions on X"`

This is **knowledge capital accumulation**.

### Weekly Organization

Once per week:

1. Run: `ORGANIZE knowledge blocks`
2. Review proposed merges
3. Update themes
4. Normalize tags
5. Commit organization changes

---

## Best Practices

### ✅ Do

- **Extract immediately** when you spot value
- **One idea per block** — Keep blocks atomic
- **Use semantic names** — Future you will thank you
- **Reference blocks** when assembling
- **Commit regularly** — Git is your memory
- **Review confidence** — Keep it calibrated

### ❌ Don't

- **Save full chat logs** — Extract instead
- **Rewrite the same idea** — Reuse blocks
- **Generate without blocks** — Extract first
- **Mix thinking and publishing** — Separate concerns
- **Let insights die** — Extract or lose them
- **Use project names** — Use stable concepts

### Anti-Patterns to Avoid

1. **Archive everything** — Only extract valuable insights
2. **Rewrite from scratch** — Assemble from blocks
3. **Skip extraction** — "I'll do it later" = lost knowledge
4. **Mix concerns** — Keep thinking and publishing separate
5. **Ignore organization** — Chaos accumulates quickly

---

## Troubleshooting

### "I can't find a block I need"

**Solution:** Extract it first. Don't generate content without blocks.

### "I have duplicate blocks"

**Solution:** Run `ORGANIZE` to identify and merge duplicates.

### "Themes are getting messy"

**Solution:** Run `ORGANIZE` to normalize themes. Use stable concepts, not projects.

### "Assembler says blocks are insufficient"

**Solution:** Extract more blocks on the topic. Don't ask Assembler to generate.

### "I don't know what to extract"

**Ask yourself:**
- Is this a clear conclusion?
- Is this a reusable framework?
- Is this actionable (checklist)?
- Is this a strong narrative/metaphor?

If none → don't extract. It's just thinking out loud.

### "Blocks seem too granular"

**Reality check:** Blocks should be atomic. You can always assemble multiple blocks. Granularity enables reuse.

---

## Summary

KOS transforms conversations into a reusable knowledge system:

1. **Extract** valuable insights → blocks
2. **Organize** periodically → coherence
3. **Assemble** when needed → content

Remember: **If it isn't a block, it isn't real.**

You're not producing text. You're building a long-term thinking engine.


# Knowledge Operating System (KOS)

This repository is **not an archive of chats**.  
It is a **system for extracting, organizing, and reusing thinking**.

Chats are ephemeral.  
Knowledge blocks are capital.  
Content is assembled, not rewritten.

---

## Core Principles

1. **Chats are raw material**
2. **Blocks are truth**
3. **Candidates are intent**
4. **Outputs are assemblies**
5. **Nothing valuable lives only in chat history**

If an idea is not extracted into a block, it does not exist.

---

## Repository Structure


```
knowledge/
blocks/ # Atomic, reusable knowledge (source of truth)
conclusions/
frameworks/
checklists/
narratives/
metaphors/

candidates/ # Potential content units (structure, not prose)
book/
chapters/
sections/
articles/
posts/

pipelines/ # Routing rules (what goes where)
knowledge/pipelines/pipeline.yaml

themes/ # Theme definitions (stable concepts)

AGENTS.md # Agent instructions

output/ # Generated content (never edited manually)
blog/
book/
email/
diary/
```

---

## Mental Model

- **Chat** → thinking space  
- **Extractor** → turns thinking into blocks  
- **Organizer** → maintains order and coherence  
- **Candidates** → potential chapters, articles, posts  
- **Assembler** → builds content from blocks  
- **Git** → long-term memory  

You do not “write content”.  
You **build a knowledge system that produces content**.

---

## Knowledge Blocks (`knowledge/blocks/`)

Blocks are **atomic** and **reusable**.

### Block rules
- One idea per file
- No dates in filenames
- No project-specific naming
- Written to be reused blindly by another agent

### Block types
- `conclusion` – a clear insight or decision
- `framework` – a reusable structure or model
- `checklist` – actionable steps
- `narrative` – story, vignette, or example
- `metaphor` – conceptual compression

Blocks always include frontmatter:
```yaml
type: conclusion
themes: [ai-agents]
confidence: high
reuse: [blog, book, email]
tags: [ai, agents]
```

## Content Candidates (`knowledge/candidates/`)

Candidates represent potential content, not finished text.

They answer:

- "This could be a chapter"
- "This should be an article"
- "This is at least a blog post"

### Candidate types

- book_chapter
- book_section
- article
- blog_post

Candidates:

- reference existing blocks
- define structure and intent
- evolve via status changes

### Candidate lifecycle

draft → solid → used → deprecated

Nothing is deleted.
History matters.

## Pipelines (`knowledge/pipelines/`)

Pipelines define where blocks are allowed to go.

Examples:

Blog → public, medium confidence

Book → deep, high confidence only

Email → short, compressed

Diary → private, unrestricted

Pipelines:

- never generate ideas
- never override blocks
- only assemble

## Agents

### Extractor

- Triggered during or after thinking
- Extracts conclusions, frameworks, checklists
- Can also mark content candidates

### Organizer

- Maintains themes, tags, duplication control
- Merges or deprecates blocks (never deletes)
- Keeps the system navigable

### Assembler

- Builds blog posts, chapters, emails
- Uses existing blocks only
- Always includes source references

Agents are functions, not personalities.

## Cursor Workflow

Typical loop:

- Think in chat
- Spot value
- EXTRACT → create block
- Periodically ORGANIZE
- When needed: ASSEMBLE → output

If something is missing:

- you extract more blocks
- you do not regenerate content from scratch

## Anti-Patterns (Strictly Avoid)

- Saving full chat logs
- Rewriting the same idea twice
- Generating content without blocks
- Mixing thinking and publishing
- Letting insights die in chat history

## Why This Exists

This system exists to:

- eliminate repeated thinking
- turn conversations into assets
- support books, blogs, consulting, and products
- scale thinking without losing coherence

You are not producing text.  
You are building a long-term thinking engine.

## One Rule to Remember

If it isn't a block, it isn't real.
# Getting Started with Knowledge Operating System (KOS)

Welcome to KOS — a system for extracting, organizing, and reusing thinking from your conversations.

## What is KOS?

KOS transforms ephemeral chat conversations into durable, reusable knowledge blocks. Instead of losing insights in chat history, you build a knowledge system that produces content.

**Key principle:** If it isn't a block, it isn't real.

## Quick Setup

### 1. Initialize Repository Structure

Create the following directory structure:

```
knowledge/
  blocks/
    conclusions/
    frameworks/
    checklists/
    narratives/
    metaphors/
  candidates/
    book/
    chapters/
    sections/
    articles/
    posts/
  pipelines/
  themes/
AGENTS.md
output/
  blog/
  book/
  email/
  diary/
```

### 2. Understand the Workflow

The core workflow is simple:

**Chat → Extract → Organize → Assemble**

- **Chat**: Think and discuss (ephemeral)
- **Extract**: Turn valuable insights into blocks
- **Organize**: Maintain coherence and prevent duplication
- **Assemble**: Build content from existing blocks

### 3. Your First Extraction

When you have a valuable insight in a conversation:

1. Signal extraction: Type `EXTRACT conclusion` (or other block type)
2. The Extractor agent will:
   - Evaluate if it's worth extracting
   - Choose the appropriate block type
   - Create a file in `knowledge/blocks/`

Example commands:
```
EXTRACT conclusion
EXTRACT framework
EXTRACT checklist
```

**Russian aliases:**
- ИЗВЛЕЧЬ вывод → EXTRACT conclusion
- ИЗВЛЕЧЬ фреймворк → EXTRACT framework

### 4. Your First Assembly

When you need content:

1. Request assembly: `ASSEMBLE blog theme: ai-agents length: medium`
2. The Assembler agent will:
   - Find relevant blocks
   - Check reuse permissions
   - Assemble content
   - Add source references

## Core Concepts

### Knowledge Blocks

Blocks are atomic, reusable units of knowledge. Each block:
- Contains one idea
- Has frontmatter metadata
- Can be reused across different outputs

### Block Types

- **conclusion**: Clear insight or decision
- **framework**: Reusable structure or model
- **checklist**: Actionable steps
- **narrative**: Story, vignette, or example
- **metaphor**: Conceptual compression

### Agents

Three agents handle different aspects:

- **Extractor**: Creates blocks from conversations
- **Organizer**: Maintains system coherence
- **Assembler**: Builds content from blocks

## Next Steps

- Read the [User Guide](User-Guide.md) for detailed instructions
- Check the [Quick Reference](Quick-Reference.md) for common commands
- Review [AGENTS.md](../AGENTS.md) for agent specifications

## Important Rules

✅ **Do:**
- Extract valuable insights immediately
- One idea per block
- Use semantic filenames (kebab-case)
- Reference blocks when assembling

❌ **Don't:**
- Save full chat logs
- Rewrite the same idea twice
- Generate content without blocks
- Mix thinking and publishing

Remember: You're building a knowledge system, not just writing text.


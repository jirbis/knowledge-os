# KOS Documentation Index

Complete index of all Knowledge Operating System (KOS) documentation.

---

## 📚 Documentation Files

### Getting Started

- **[Getting Started](Getting-Started.md)**  
  Quick setup guide for new users. Learn what KOS is, set up your repository, and perform your first extraction and assembly.

### User Documentation

- **[User Guide](User-Guide.md)**  
  Complete reference guide covering:
  - KOS philosophy and mental model
  - Working with knowledge blocks
  - Using agents (Extractor, Organizer, Assembler, ArchiveSearch, SUGGEST)
  - Content candidates and pipelines
  - Daily workflow and best practices
  - Troubleshooting

- **[Quick Reference](Quick-Reference.md)**  
  Command cheat sheet with:
  - All agent commands (EXTRACT, ORGANIZE, ASSEMBLE, SUGGEST, MARK, SET)
  - Block types and frontmatter templates
  - File naming conventions
  - Common patterns and workflows
  - Daily and weekly checklists

- **[Cursor Workflow](Cursor%20Workflow.md)**  
  Detailed Cursor IDE workflow guide (in Russian). Step-by-step instructions for using KOS in Cursor.

---

## 🔗 Related Documentation

### Core System Files

- **[COMMANDS.md](../COMMANDS.md)**  
  **Single source of truth** for all commands. Defines canonical commands and Russian aliases. If a command is not here, it doesn't exist.

- **[AGENTS.md](../AGENTS.md)**  
  Agent constitution and global rules. Defines philosophy, source-of-truth hierarchy, and contracts for all agents.

- **[AGENTS/](../AGENTS/)**  
  Individual agent specifications:
  - `AGENTS/Extractor.md` — Extraction rules and command normalization
  - `AGENTS/Organizer.md` — Organization and coherence rules
  - `AGENTS/Assembler.md` — Assembly rules and pipeline compliance
  - `AGENTS/ArchiveSearch.md` — Archive search and indexing rules

- **[README.md](../README.md)**  
  Project overview and core principles. High-level introduction to KOS philosophy and structure.

- **[WORKFLOW.md](../WORKFLOW.md)**  
  Basic workflow overview (in Russian).

---

## 🗂️ Documentation Structure

```
docs/
  index.md              # This file (complete index)
  README.md             # Documentation overview
  Getting-Started.md    # Quick start guide
  User-Guide.md         # Comprehensive user guide
  Quick-Reference.md    # Command reference
  Cursor Workflow.md    # Cursor IDE workflow (Russian)
  anti-patterns.md      # Anti-patterns checklist
  examples-session.md    # Real usage examples

../
  COMMANDS.md           # Command specifications (single source of truth)
  AGENTS.md             # Agent constitution (global rules)
  AGENTS/               # Individual agent specifications
    Extractor.md
    Organizer.md
    Assembler.md
    ArchiveSearch.md
  README.md             # Project overview
  WORKFLOW.md           # Basic workflow
  knowledge/
    pipelines/
      pipeline.yaml     # Pipeline configuration
```

---

## 🚀 Quick Navigation

**I want to...**

- **Start using KOS** → [Getting Started](Getting-Started.md)
- **Learn everything** → [User Guide](User-Guide.md)
- **Look up a command** → [Quick Reference](Quick-Reference.md)
- **See all commands** → [COMMANDS.md](../COMMANDS.md)
- **Understand agent rules** → [AGENTS.md](../AGENTS.md)
- **See agent specs** → [AGENTS/](../AGENTS/)
- **Use Cursor workflow** → [Cursor Workflow](Cursor%20Workflow.md)
- **Get project overview** → [README.md](../README.md)
- **Check examples** → [Examples Session](examples-session.md)
- **Review anti-patterns** → [Anti-Patterns](anti-patterns.md)

---

## 📖 Documentation by Topic

### Commands

- [COMMANDS.md](../COMMANDS.md) — Complete command reference
- [Quick Reference](Quick-Reference.md) — Command cheat sheet
- [User Guide: Using Agents](User-Guide.md#using-agents) — Detailed agent usage

### Agents

- [AGENTS.md](../AGENTS.md) — Agent constitution and global rules
- [AGENTS/Extractor.md](../AGENTS/Extractor.md) — Extraction agent specification
- [AGENTS/Organizer.md](../AGENTS/Organizer.md) — Organization agent specification
- [AGENTS/Assembler.md](../AGENTS/Assembler.md) — Assembly agent specification
- [AGENTS/ArchiveSearch.md](../AGENTS/ArchiveSearch.md) — Archive search agent specification
- [User Guide: Using Agents](User-Guide.md#using-agents) — How to use agents
- [Quick Reference: Agent Commands](Quick-Reference.md#agent-commands) — Command quick lookup

### Knowledge Blocks

- [User Guide: Working with Knowledge Blocks](User-Guide.md#working-with-knowledge-blocks) — Complete guide
- [Quick Reference: Block Types](Quick-Reference.md#block-types) — Block type reference
- [Getting Started: Core Concepts](Getting-Started.md#core-concepts) — Introduction

### Workflow

- [Cursor Workflow](Cursor%20Workflow.md) — Cursor IDE workflow (Russian)
- [User Guide: Daily Workflow](User-Guide.md#daily-workflow) — Workflow patterns
- [Quick Reference: Workflow Pattern](Quick-Reference.md#workflow-pattern) — Quick reference

### Content Candidates

- [User Guide: Content Candidates](User-Guide.md#content-candidates) — Complete guide
- [Quick Reference: Candidate Lifecycle](Quick-Reference.md#candidate-lifecycle) — Lifecycle reference

### Pipelines

- [User Guide: Pipelines](User-Guide.md#pipelines) — Pipeline configuration
- [README.md: Pipelines](../README.md#pipelines-knowledgepipelines) — Overview
- Pipeline file: `knowledge/pipelines/pipeline.yaml`

### Archive Search

- [AGENTS/ArchiveSearch.md](../AGENTS/ArchiveSearch.md) — Archive search specification
- [User Guide: ArchiveSearch](User-Guide.md#archive-search) — Using archive search
- [Quick Reference: Search Archive](Quick-Reference.md#search-archive) — Command reference

---

## 🎯 Key Concepts

- **Knowledge Blocks**: Atomic, reusable units of knowledge
- **Agents**: Extractor, Organizer, Assembler, ArchiveSearch, SUGGEST
- **Workflow**: Chat → Extract → Organize → Assemble
- **Archive Search**: Memory system for finding past conversations
- **Core Principle**: If it isn't a block, it isn't real

---

## 📝 Documentation Status

All documentation files are:
- ✅ Up to date with COMMANDS.md
- ✅ Consistent command formats
- ✅ Cross-referenced
- ✅ Lint-checked

---

**Start here:** [Getting Started](Getting-Started.md)


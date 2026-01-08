# Quick Reference: KOS Commands and Patterns

Quick lookup guide for common KOS operations.

## Agent Commands

### Extractor

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

**Output:** Creates file in `knowledge/blocks/{type}/`

### Organizer

```
ORGANIZE knowledge blocks
ORGANIZE themes
ORGANIZE duplicates
```

**Russian aliases:**
- ОРГАНИЗОВАТЬ блоки → ORGANIZE knowledge blocks
- ОРГАНИЗОВАТЬ темы → ORGANIZE themes
- ОРГАНИЗОВАТЬ дубликаты → ORGANIZE duplicates

**Output:** Proposes changes, updates metadata

### Assembler

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

**Output:** Creates file in `output/{type}/`

---

## Block Types

| Type | Use When | Example |
|------|----------|---------|
| `conclusion` | Clear insight or decision | "AI agents need executable protocols" |
| `framework` | Reusable structure | Protocol structure, decision tree |
| `checklist` | Actionable steps | Extraction workflow, review process |
| `narrative` | Story or example | Case study, vignette |
| `metaphor` | Conceptual compression | "Blocks are LEGO bricks" |

---

## Frontmatter Template

```yaml
---
type: conclusion
themes:
  - primary-theme
  - secondary-theme
confidence: high
reuse:
  - blog
  - book
  - email
source: chat
tags:
  - tag1
  - tag2
---
```

---

## File Naming

✅ **Good:**
- `jira-workflows-vs-ai-protocols.md`
- `executable-protocol-structure.md`
- `knowledge-extraction-checklist.md`

❌ **Bad:**
- `notes-2024-01-15.md` (dates)
- `client-x-insight.md` (project name)
- `thoughts.md` (generic)

---

## Confidence Levels

- **high**: Well-tested, proven, certain
- **medium**: Reasonable confidence, some evidence
- **low**: Speculative, hypothesis, needs validation

---

## Reuse Targets

- `blog`: Public blog posts
- `book`: Book chapters/sections
- `email`: Email content
- `consulting`: Client-facing materials
- `diary`: Private notes

---

## Candidate Lifecycle

```
draft → solid → used → deprecated
```

- **draft**: Initial structure
- **solid**: Ready for assembly
- **used**: Already assembled
- **deprecated**: No longer relevant

---

## Daily Checklist

- [ ] Extract valuable insights from conversations
- [ ] Review new blocks
- [ ] Update confidence if needed
- [ ] Commit changes: `git commit -m "Extracted X"`

## Weekly Checklist

- [ ] Run `ORGANIZE knowledge blocks`
- [ ] Review proposed merges
- [ ] Normalize themes
- [ ] Update tags
- [ ] Commit organization changes

---

## Workflow Pattern

```
Chat → Extract → Organize → Assemble
```

1. **Chat**: Think (ephemeral)
2. **Extract**: Create blocks (durable)
3. **Organize**: Maintain coherence (periodic)
4. **Assemble**: Build content (on demand)

---

## Common Patterns

### Pattern: Extract Conclusion

```
EXTRACT conclusion
```

### Pattern: Extract Framework

```
EXTRACT framework
```

### Pattern: Assemble Blog Post

```
ASSEMBLE blog
theme: [theme-name]
length: medium
```

### Pattern: Assemble Article

```
ASSEMBLE article
themes: [theme1], [theme2]
tone: deep
```

### Pattern: Suggest Extraction

```
SUGGEST extract
```

### Pattern: Mark Candidate

```
MARK as book_chapter candidate
MARK as blog_post candidate
```



## Anti-Patterns

❌ Don't:
- Save full chat logs
- Rewrite the same idea
- Generate without blocks
- Mix thinking and publishing
- Use project names in themes

✅ Do:
- Extract immediately
- One idea per block
- Semantic filenames
- Reference blocks
- Commit regularly

---

## Additional Commands

### SUGGEST (advisory only, no file creation)

```
SUGGEST extract
SUGGEST organization
SUGGEST assembly
```

**Russian aliases:**
- ПРЕДЛОЖИ извлечение → SUGGEST extract
- ПРЕДЛОЖИ организацию → SUGGEST organization
- ПРЕДЛОЖИ сборку → SUGGEST assembly

### MARK (content candidates)

```
MARK as book_chapter candidate
MARK as book_section candidate
MARK as article candidate
MARK as blog_post candidate
```

**Russian aliases:**
- ОТМЕТИТЬ как главу → MARK as book_chapter candidate
- ОТМЕТИТЬ как статью → MARK as article candidate
- ОТМЕТИТЬ как пост → MARK as blog_post candidate

### SET (candidate status)

```
SET status: draft
SET status: solid
SET status: used
SET status: deprecated
```

**Russian aliases:**
- УСТАНОВИТЬ статус: draft → SET status: draft
- УСТАНОВИТЬ статус: solid → SET status: solid
- УСТАНОВИТЬ статус: used → SET status: used
- УСТАНОВИТЬ статус: deprecated → SET status: deprecated

## Search Archive {#search-archive}

### SEARCH (archive search, read-only)

```
SEARCH archive export_path=/path/to/conversations.json query="search terms" limit=20
```

**Parameters:**
- `export_path`: Path to ChatGPT export file (required on first run)
- `query`: FTS5 search query (required)
- `limit`: Number of results (optional, default 20)
- `reindex`: Force reindexing (optional, default false)

**Russian aliases:**
- ПОИСК архив → SEARCH archive
- НАЙТИ в архиве → SEARCH archive

**Output:** Search results with conversation IDs and snippets. Never creates knowledge blocks.

**Next steps after search:**
1. Extract snippet: `python3 tools/extract_snippet.py --id <conversation_id>`
2. Suggest extraction: `SUGGEST extract`
3. Extract if confirmed: `ИЗВЛЕЧЬ вывод` / `ИЗВЛЕЧЬ чеклист` / etc.

---

## Key Principle

> **If it isn't a block, it isn't real.**

Extract or lose it.



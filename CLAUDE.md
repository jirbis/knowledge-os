# Knowledge-OS Architecture Reference

This document provides a comprehensive reference for AI agents operating within the Knowledge-OS repository architecture.

---

## Repository Overview

**Repository Type**: Knowledge-OS (Constitutional Agent Architecture)
**Primary Purpose**: Systematic knowledge extraction, organization, and assembly
**Architecture**: Constitutional Repository with explicit rules, roles, and enforcement mechanisms

---

## 1. Constitutional Rules (Canons)

### Primary Rule Files

#### `.cursor/rules.md`
**Location**: `.cursor/rules.md`
**Purpose**: Canonical rules that apply to all commands and agent operations

**Key Principles**:
- Commands are explicit and not guessed
- Any action must go through a command
- Without a command → discussion only
- `SUGGEST` never writes anything
- Only commands defined in `.cursor/commands/` are valid

**Core Rules Summary**:
1. **Command Authority** — Only commands in `.cursor/commands/` are valid
2. **Allowed Write Locations** — `./blocks/`, `./export/`, `./import/normalized/`, `./index/`
3. **Block Rules** — One block = one idea; blocks must be reusable; deletion forbidden
4. **Safety and Reversibility** — All operations reversible via git; prefer no-op over risky action
5. **One Rule Above All** — "If it is not in a block, it does not exist"

### Configuration

#### `config.yaml`
**Location**: `./config.yaml`
**Purpose**: Pipeline configuration and boundary enforcement

**Key Settings**:
```yaml
boundaries:
  protected_paths:
    - ./blocks  # Protected — read-only for pipeline
  allowed_output_paths:
    - ./export  # Allowed — write operations permitted
  validate_before_assembly: true

embeddings:
  model: openai
  database: ./index/embeddings.sqlite
  chunk_size: 512
  chunk_overlap: 64
```

---

## 2. Agent Roles and Commands

### Command Files Directory
**Location**: `.cursor/commands/`

All canonical commands are defined here:

#### Available Commands

| Command | File | Role | Write Permission |
|---------|------|------|-----------------|
| `EXTRACT` | `extract.md` | Extract knowledge blocks from conversations | `./blocks/` only |
| `ASSEMBLE` | `assemble.md` | Assemble content from blocks | `./export/` only |
| `ORGANIZE` | `organize.md` | Suggest organization improvements | Suggest only (no write) |
| `SEARCH` | `search.md` | Import and search conversations | `./import/normalized/`, `./index/` |
| `SUGGEST` | `suggest.md` | Suggest actions without executing | Read-only |
| `STATUS` | `status.md` | Candidate state management | Status tracking |
| `HELP` | `help.md` | Command help | Read-only |

### Agent Roles (from Constitutional Framework)

From `blocks/frameworks/constitutional-agent-architecture.md`:

- **ORCHESTRATOR**: Coordinates tasks and CHECK protocol
- **CODER**: Implements changes strictly from architecture
- **ARCHITECTURE_CURATOR**: Proposes controlled evolution (proposals only)
- **CHECKER**: Executes CHECK protocol

---

## 3. Paths and Boundaries

### Protected Paths (Read-Only)
**Defined in**: `config.yaml` → `boundaries.protected_paths`

- `./blocks/` — Knowledge blocks (source of truth)
  - `./blocks/frameworks/` — Reusable structures and models
  - `./blocks/checklists/` — Actionable step lists
  - `./blocks/conclusions/` — Clear insights and decisions
  - `./blocks/narratives/` — Stories and examples
  - `./blocks/plans/` — Action plans for humans
  - `./blocks/patterns/` — Repeatable patterns

### Allowed Write Paths
**Defined in**: `config.yaml` → `boundaries.allowed_output_paths`

- `./export/` — Assembled content output
  - `./export/book/` — Book content
- `./import/normalized/` — Normalized markdown for search indexing
- `./index/` — Search databases
  - `./index/embeddings.sqlite` — Semantic search embeddings
  - `./index/chats.sqlite` — FTS5 full-text search

### Validation Tool
**Location**: `tools/validate_repository_boundaries.py`

**Usage**:
```bash
# Check if a path is protected
python3 tools/validate_repository_boundaries.py --check-path ./blocks

# Validate configuration
python3 tools/validate_repository_boundaries.py
```

---

## 4. Gates and Validation (Check/Pass/Fail)

### Constitutional Compliance Gates

#### Direct Push Command Gate
**Location**: `blocks/checklists/direct-push-command-gate-safety-requirements.md`

**Purpose**: Ensure only canonical commands can cause writes, with full auditability

**Checklist**:
- [ ] Command authority (canonical command set exists)
- [ ] Authentication & permissions (GitHub App with minimal scope)
- [ ] Branching & overwrite policy (day branches, no overwrites)
- [ ] Path safety & boundaries (explicit allowed paths)
- [ ] Auditability & reversibility (full logging)
- [ ] Rate limits & abuse controls

**Pass Condition**: Direct push cannot happen unless valid command accepted, with full audit metadata

#### Constitutional Compliance Checklist
**Location**: `blocks/checklists/constitutional-compliance-checklist.md`

**Core Validity Conditions**:
- [ ] ARCHITECTURE.md exists and is parseable
- [ ] TASK_GRAPH defined
- [ ] Agent roles explicitly defined
- [ ] Ownership mapping complete
- [ ] CHECK executable and produces deterministic report
- [ ] Proposal mechanism established
- [ ] CHECK PASS achieved

#### Knowledge-OS Validation Workflows
**Location**: `blocks/checklists/knowledge-os-validation-workflows.md`

**Validation Types**:
1. Block Integrity Validation
2. Repository Boundary Validation
3. Configuration Validation
4. Command Validation
5. CI/CD Validation
6. Comprehensive Validation Workflow

---

## 5. Frameworks and Patterns

### Core Architectural Frameworks

#### Constitutional Agent Architecture
**Location**: `blocks/frameworks/constitutional-agent-architecture.md`

**Core Principles**:
1. Protocol-First — Actions over states
2. Artifact-First — Files are system memory
3. Role-Based Execution — Explicit contracts
4. Fail-Fast Enforcement — CHECK Protocol as barrier
5. Occam-Governed Evolution — Complexity must be justified
6. Decoupled by Design — Reimplementation without author

#### Agentic Repository Architecture Doctrine
**Location**: `blocks/frameworks/agentic-repository-architecture-doctrine.md`

**Key Features**:
- Mandatory artifacts (architecture, task graph, agent roles, proposals, CHECK)
- Agent roles with ownership mapping
- TASK_GRAPH contract
- CHECK Protocol (constitutional barrier)
- Proposal mechanism
- OCCAM Rules (anti-entropy)

#### Agent Roles, Not Minds
**Location**: `blocks/frameworks/agent-roles-not-minds.md`

**Claim**: Agents must be deterministic roles with strict contracts, not creative minds

**Why Constraints Increase Freedom**:
- Eliminate ambiguity
- Enable composition
- Focus creative energy
- Prevent chaos

#### OCCAM Rules (Anti-Entropy)
**Location**: `blocks/frameworks/occam-rules-anti-entropy.md`

**Five Rules**:
1. **OCCAM-1**: New moving parts require necessity proof
2. **OCCAM-2**: Configuration over code
3. **OCCAM-3**: One proposal, one purpose
4. **OCCAM-4**: Deletion is default
5. **OCCAM-5**: Enforcement must remain simple

**Enforcement**: If any OCCAM rule violated, CHECK fails

### Patterns

#### Canonical Proposal Structure
**Location**: `blocks/patterns/canonical-proposal-structure.md`

Standard structure for evolution proposals (P0, P1, P2)

#### Task Graph Development Workflow
**Location**: `blocks/patterns/task-graph-development-workflow.md`

Workflow pattern for task-based development

---

## 6. Tools and Scripts

### Tool Directory
**Location**: `./tools/`

#### Semantic Search Tools
- `embed_blocks.py` — Generate embeddings for semantic search
- `semantic_search.py` — Query embeddings
- `read_block.py` — Read single block with metadata
- `assemble_blocks.py` — Combine multiple blocks

#### Validation Tools
- `validate_repository_boundaries.py` — Enforce boundaries and protected paths

#### Repository Management
- `init_repository.py` — Initialize repository structures

#### Archive & Search (FTS5)
- `ingest_chatgpt_export.py` — Ingest ChatGPT exports
- `search_archive.py` — Search indexed conversations
- `extract_snippet.py` — Extract conversation snippets

### Tool Documentation
**Location**: `tools/README.md`

---

## 7. Block Types and Schemas

### Block Type Definitions

From `.cursor/rules.md` § 4:

| Type | Purpose | Example Use |
|------|---------|-------------|
| `conclusion` | Clear insight or decision | Market analysis results |
| `framework` | Reusable structure or model | Constitutional architecture |
| `checklist` | Actionable steps | Validation workflows |
| `narrative` | Story, vignette, or example | Case studies |
| `metaphor` | Conceptual compression | Analogies |
| `plan` | Action plan for human | Next steps, tasks |

### Block Integrity Rules

**From `.cursor/rules.md` § 4**:
- One block = one idea
- Blocks MUST be reusable without context
- Blocks MUST contain frontmatter
- Deletion is forbidden (only deprecation allowed)
- Blocks MUST be saved ONLY in `blocks/`
- Blocks MUST NOT be saved in other repositories

### Block Frontmatter Schema

```yaml
---
type: framework|checklist|conclusion|narrative|metaphor|plan
themes:
  - theme-one
  - theme-two
confidence: high|medium|low
reuse:
  - blog
  - book
  - documentation
source: chat|agentic-repository-architecture|constitution-driven-agent-automation-book
tags:
  - tag-one
  - tag-two
---
```

---

## 8. Operating Procedures

### Command Execution Flow

1. **User Input** → Natural language or explicit command
2. **Command Normalization** → Match to canonical commands in `.cursor/commands/`
3. **Validation** → Verify command syntax and permissions
4. **Execution** → Perform action within boundaries
5. **Verification** → Validate output and compliance

### Write Operation Safety Protocol

**Before ANY write operation**:
1. Validate command authority (is it a canonical command?)
2. Check path boundaries (is target path allowed?)
3. Run `validate_repository_boundaries.py --check-path <target>`
4. Verify no protected paths modified
5. Execute write
6. Verify write succeeded
7. Log action for audit trail

### Stop Conditions (Must Refuse)

From `.cursor/rules.md` § 7:

Agents must stop when:
- Asked to write outside allowed dirs
- Asked to generate new ideas/examples/claims
- Asked to modify blocks without explicit command
- User requests "creativity" for Assembler/Extractor
- Command is ambiguous or malformed

**Response**: "Stopping: this action violates Knowledge-OS rules."

---

## 9. Meaning Safety Rules

From `.cursor/rules.md` § 8:

- **No invention**: Agents cannot create new claims
- **No drift**: Assembled content must match blocks exactly
- **No style rewriting**: Follow STYLE.md if present
- **One source of truth**: blocks → export
- **No cross-contamination**: blocks never go into export repo; chats never go into blocks
- **Repository boundaries**: Always validate paths using `tools/validate_repository_boundaries.py`

---

## 10. Proposal and Evolution Mechanism

### Proposal Lifecycle

From `blocks/frameworks/agentic-repository-architecture-doctrine.md`:

```
Observe → Propose → Review → Approve → Apply → Record
```

### Proposal Types

- **P0**: Clarifications (no change to rules)
- **P1**: Standard changes
- **P2**: Complexity increases (requires Occam Test)

### P2 Requirements

P2 proposals must include:
1. Occam Test (required section)
2. Necessity demonstration
3. Justification for every moving part added
4. Complexity budget
5. Reversal plan

---

## 11. CHECK Protocol

### Constitutional Barrier

From `blocks/frameworks/constitutional-agent-architecture.md`:

- CHECK Protocol is a constitutional barrier (not optional)
- No task marked `done` without CHECK PASS
- Architecture changes invalidate previous CHECK PASS
- Execution halts on CHECK FAIL
- Produces `check_report.md` or `check_report.json` at repo root

### What CHECK Validates

- Constitutional compliance
- OCCAM compliance
- Ownership boundaries
- Proposal format
- Path boundaries
- Block integrity

---

## 12. Quick Reference

### Essential Files

| File | Purpose | Type |
|------|---------|------|
| `.cursor/rules.md` | Canonical rules | Canon (Law) |
| `.cursor/commands/*.md` | Command definitions | Canon (Law) |
| `config.yaml` | Pipeline & boundaries | Configuration |
| `tools/validate_repository_boundaries.py` | Boundary enforcement | Gate |
| `blocks/checklists/direct-push-command-gate-safety-requirements.md` | Write safety gate | Gate |
| `blocks/checklists/constitutional-compliance-checklist.md` | Compliance gate | Gate |
| `blocks/checklists/knowledge-os-validation-workflows.md` | Validation procedures | Path |
| `blocks/frameworks/constitutional-agent-architecture.md` | Core architecture | Framework |
| `blocks/frameworks/agentic-repository-architecture-doctrine.md` | Repository doctrine | Framework |
| `blocks/frameworks/agent-roles-not-minds.md` | Agent philosophy | Framework |
| `blocks/frameworks/occam-rules-anti-entropy.md` | Complexity control | Framework |

### Command Quick Reference

```bash
# Extract knowledge
EXTRACT conclusion
EXTRACT framework
EXTRACT checklist
EXTRACT narrative
EXTRACT plan

# Assemble content
ASSEMBLE <target>

# Organize (suggest only)
ORGANIZE

# Search
SEARCH <query>

# Suggest (read-only)
SUGGEST extract
SUGGEST organize
SUGGEST assemble

# Status
STATUS

# Help
HELP
```

### Validation Quick Reference

```bash
# Validate path boundaries
python3 tools/validate_repository_boundaries.py --check-path <path>

# Semantic search
python3 tools/semantic_search.py -q "query" -t frameworks

# Read block
python3 tools/read_block.py <block_id>

# Assemble blocks
python3 tools/assemble_blocks.py -b <block_ids> -o <output>
```

---

## 13. Agent Operating Constraints

### Absolute Constraints

1. **Never write outside**: `./blocks/`, `./export/`, `./import/normalized/`, `./index/`
2. **Never modify blocks** without explicit EXTRACT command
3. **Never invent content** — extract or assemble only
4. **Never bypass** command normalization
5. **Never execute** natural language as command without confirmation
6. **Always validate** paths before write operations
7. **Always log** actions for audit trail

### Recommended Practices

1. Use semantic search before extracting (avoid duplicates)
2. Read existing blocks before creating new ones
3. Validate boundaries before write operations
4. Ask for clarification when command is ambiguous
5. Stop and report when rules are unclear
6. Prefer no-op over risky action

---

## Version

**Document Version**: 1.0
**Last Updated**: 2026-02-13
**Architecture Version**: Constitutional Agent Architecture
**Repository**: knowledge-os

---

## References

- **Constitutional Agent Architecture**: `blocks/frameworks/constitutional-agent-architecture.md`
- **Agentic Repository Architecture Doctrine**: `blocks/frameworks/agentic-repository-architecture-doctrine.md`
- **Canonical Rules**: `.cursor/rules.md`
- **Command Definitions**: `.cursor/commands/`
- **Tools Documentation**: `tools/README.md`

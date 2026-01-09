свюю# How to Connect Repositories

Practical guide for setting up directory structure and connecting repositories in Knowledge OS.

---

## Directory Structure Options

### Option 1: Monorepo (Current Structure)

**Simplest structure** — everything in one repository:

```
~/Documents/GitHub/knowlege-os/
├── knowledge/          # Semantic layer
│   ├── blocks/
│   ├── candidates/
│   └── pipelines/
├── output/             # Build output
├── drafts/             # Drafts
├── archive/            # Chat archive
└── config.yaml         # Configuration (monorepo)
```

**When to use:**
- ✅ Simplicity is more important than separation
- ✅ Privacy is not required for knowledge layer
- ✅ Everything in one place

**How to set up:**
You already have this! Just make sure `config.yaml` contains:
```yaml
architecture: "monorepo"
knowledge:
  root_path: "./knowledge"
  integration: "internal"
```

---

### Option 2: Dual-Repo (Recommended)

**Two separate repositories** — for privacy and reusability:

```
~/Documents/GitHub/
├── knowlege-os/              # Main system (public/private)
│   ├── AGENTS/
│   ├── tools/
│   ├── output/
│   ├── drafts/
│   └── config.yaml           # → ../knowledge-base/knowledge
│
└── knowledge-base/           # Semantic layer (private)
    └── knowledge/
        ├── blocks/
        ├── candidates/
        ├── INVARIANTS.md
        └── DECISIONS.md
```

**When to use:**
- ✅ Need privacy for knowledge layer
- ✅ Want to reuse knowledge across multiple projects
- ✅ Need strict separation

**How to set up:**

#### Step 1: Create directory structure

```bash
# Go to parent directory
cd ~/Documents/GitHub/

# Create knowledge-base directory (if it doesn't exist)
mkdir knowledge-base
cd knowledge-base
git init

# Initialize knowledge-base repository
python3 ../knowlege-os/tools/init_repository.py knowledge-base .

# Return to main repository
cd ../knowlege-os
```

#### Step 2: Configure connection

```bash
# In knowlege-os directory, set up dual-repo
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge
```

This will create `config.yaml` with:
```yaml
architecture: "dual-repo"
knowledge:
  root_path: "../knowledge-base/knowledge"
  integration: "external"
  read_only: true
```

#### Step 3: Move knowledge/ (if needed)

If you already have `knowledge/` in `knowlege-os`, you can move it:

```bash
# In knowlege-os directory
# Option A: Copy contents
cp -r knowledge/* ../knowledge-base/knowledge/

# Option B: Use git subtree (if you already have commits)
# git subtree push --prefix=knowledge origin knowledge-base
```

#### Step 4: Verify connection

```bash
# Verify configuration
python3 tools/validate_repository_boundaries.py --check-knowledge-access

# Verify paths
ls ../knowledge-base/knowledge/blocks/
```

---

### Option 3: Submodule (Git Submodule)

**Git submodule** — for versioned dependencies:

```
~/Documents/GitHub/knowlege-os/
├── AGENTS/
├── tools/
├── output/
├── knowledge/           # Git submodule → ../knowledge-base
│   ├── blocks/
│   └── candidates/
└── config.yaml
```

**When to use:**
- ✅ Need to version knowledge dependencies
- ✅ Want single command for cloning
- ✅ Comfortable working with git submodules

**How to set up:**

#### Step 1: Create knowledge-base repository (if it doesn't exist)

```bash
cd ~/Documents/GitHub/
mkdir knowledge-base && cd knowledge-base
git init
python3 ../knowlege-os/tools/init_repository.py knowledge-base .
git add .
git commit -m "Initial knowledge-base repository"

# If you have a remote:
git remote add origin <your-git-url>
git push -u origin main
```

#### Step 2: Add as submodule

```bash
cd ~/Documents/GitHub/knowlege-os

# Add submodule
python3 tools/setup_dual_repo.py \
  --knowledge-path ./knowledge \
  --submodule \
  --submodule-url <git-url-to-knowledge-base>
```

Or manually:
```bash
git submodule add <git-url> knowledge
```

#### Step 3: Verify

```bash
# Initialize submodule
git submodule update --init --recursive

# Verify configuration
python3 tools/validate_repository_boundaries.py --check-knowledge-access
```

---

## Complete Structure with All Repositories

If you want complete structure with 3-5 repositories:

```
~/Documents/GitHub/
├── knowlege-os/              # Main system
│   ├── AGENTS/
│   ├── tools/
│   ├── output/
│   └── config.yaml           # → ../knowledge-base/knowledge
│
├── knowledge-base/           # Semantic layer (private)
│   └── knowledge/
│       ├── blocks/
│       ├── candidates/
│       └── INVARIANTS.md
│
├── knowledge-chat-archive/   # Chat archive (private)
│   ├── threads/
│   ├── raw/
│   └── index/
│
├── my-book-1/                # Book 1 (optional)
│   └── chapters/
│
└── knowledge-shared-templates/  # Shared templates (optional)
    └── block-templates/
```

**Creating complete structure:**

```bash
cd ~/Documents/GitHub/

# 1. Main system (already exists)
# cd knowlege-os

# 2. Knowledge base
mkdir knowledge-base && cd knowledge-base
git init
python3 ../knowlege-os/tools/init_repository.py knowledge-base .
cd ..

# 3. Chat archive
mkdir knowledge-chat-archive && cd knowledge-chat-archive
git init
python3 ../knowlege-os/tools/init_repository.py chat-archive .
cd ..

# 4. Configure connections in main repository
cd knowlege-os
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge

# 5. Update config.yaml for chat archive
# Edit config.yaml:
# chat_archive:
#   root_path: "../knowledge-chat-archive"
#   integration: "external"
#   read_only: true
```

---

## Configuring Paths in config.yaml

After creating directory structure, configure paths:

### For Dual-Repo:

```yaml
architecture: "dual-repo"

knowledge:
  root_path: "../knowledge-base/knowledge"  # Relative path
  # or absolute:
  # root_path: "/Users/gkneller/Documents/GitHub/knowledge-base/knowledge"
  integration: "external"
  read_only: true
  enforce_read_only: true

chat_archive:
  root_path: "../knowledge-chat-archive"
  integration: "external"
  read_only: true
```

### For Submodule:

```yaml
architecture: "submodule"

knowledge:
  root_path: "./knowledge"  # Submodule inside repository
  integration: "submodule"
  submodule_path: "./knowledge"
  read_only: true
```

### For Monorepo (current structure):

```yaml
architecture: "monorepo"

knowledge:
  root_path: "./knowledge"  # Inside same repository
  integration: "internal"
  read_only: false
  enforce_read_only: true  # Still validate boundaries
```

---

## Verifying Connection

After setup, verify:

```bash
# 1. Check configuration
python3 tools/validate_repository_boundaries.py --check-knowledge-access

# 2. Check specific path
python3 tools/validate_repository_boundaries.py --check-path ./output/test.md
# Should be: OK

python3 tools/validate_repository_boundaries.py --check-path ./knowledge/blocks/test.md
# Should be: ERROR (protected path)

# 3. Verify paths are readable
python3 -c "
import yaml
config = yaml.safe_load(open('config.yaml'))
print('Knowledge path:', config['knowledge']['root_path'])
print('Architecture:', config['architecture'])
"
```

---

## Common Scenarios

### Scenario 1: I already have knowlege-os with knowledge/

**Migrating to dual-repo:**

```bash
cd ~/Documents/GitHub/

# 1. Create knowledge-base separately
mkdir knowledge-base && cd knowledge-base
git init
python3 ../knowlege-os/tools/init_repository.py knowledge-base .

# 2. Copy knowledge/ contents
cp -r ../knowlege-os/knowledge/* ./knowledge/

# 3. Commit
git add .
git commit -m "Initial knowledge-base from monorepo"

# 4. Configure connection in main repository
cd ../knowlege-os
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge

# 5. (Optional) Remove knowledge/ from main repository
# git rm -r knowledge/
# Add to .gitignore if you want to keep structure
```

### Scenario 2: Starting from scratch

```bash
cd ~/Documents/GitHub/

# 1. Main system
git clone <your-knowlege-os-repo> knowlege-os
cd knowlege-os

# 2. Create knowledge-base next to it
cd ..
mkdir knowledge-base && cd knowledge-base
git init
python3 ../knowlege-os/tools/init_repository.py knowledge-base .

# 3. Configure connection
cd ../knowlege-os
python3 tools/setup_dual_repo.py --knowledge-path ../knowledge-base/knowledge
```

### Scenario 3: Using existing repositories

If you already have separate repositories:

```bash
# Just specify correct paths in config.yaml
knowledge:
  root_path: "/absolute/path/to/your-knowledge-repo/knowledge"
  # or relative:
  # root_path: "../your-custom-knowledge-repo/knowledge"
```

---

## Frequently Asked Questions

### Q: Can I use custom repository names?

**A:** Yes! Repository names are configurable:
- `knowledge-base` → can be named `semantic-repo`, `my-knowledge`, etc.
- Important: **roles** are fixed, **names** are flexible
- Just specify correct path in `config.yaml`

### Q: How to change path after setup?

**A:** Edit `config.yaml`:
```yaml
knowledge:
  root_path: "../new-path/knowledge"  # New path
```

Then verify:
```bash
python3 tools/validate_repository_boundaries.py --check-knowledge-access
```

### Q: Can I use absolute paths?

**A:** Yes, both relative and absolute paths are supported:
```yaml
# Relative (recommended)
root_path: "../knowledge-base/knowledge"

# Absolute
root_path: "/Users/gkneller/Documents/GitHub/knowledge-base/knowledge"
```

### Q: How to verify connection is working?

**A:** Use validation:
```bash
python3 tools/validate_repository_boundaries.py
```

And check path readability:
```bash
ls $(python3 -c "import yaml; c=yaml.safe_load(open('config.yaml')); print(c['knowledge']['root_path'])")/blocks/
```

---

## Next Steps

1. ✅ Choose architecture (monorepo/dual-repo/submodule)
2. ✅ Create directory structure
3. ✅ Configure `config.yaml`
4. ✅ Verify validation
5. ✅ Start working!

---

## Useful Commands

```bash
# Initialize repository
python3 tools/init_repository.py <type> <path>

# Set up dual-repo
python3 tools/setup_dual_repo.py --knowledge-path <path>

# Validate
python3 tools/validate_repository_boundaries.py

# View configuration
cat config.yaml | grep -A 5 knowledge
```

---

## Related Documentation

- [Multi-Repository Setup](Multi-Repository-Setup.md) — Complete setup guide
- [Multi-Repository Examples](Multi-Repository-Examples.md) — Integration examples
- [Framework: Private Repository Structure](../knowledge/blocks/frameworks/private-repository-structure.md) — Architecture patterns

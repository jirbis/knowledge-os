#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Consolidation Script

Consolidates fragmented themes into canonical vocabulary based on
theme-consolidation-mapping.md framework.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set
import yaml

# Consolidation mapping from theme-consolidation-mapping.md
THEME_CONSOLIDATION = {
    'knowledge-os': 'knowledge-management',
    'knowledge-systems': 'knowledge-management',
    'knowledge-extraction': 'knowledge-management',

    'repository': 'repository-architecture',
    'repository-integration': 'repository-architecture',
    'repository-governance': 'repository-architecture',

    'agents': 'agent-architecture',
    'agent-orchestration': 'agent-architecture',
    'agentic-architecture': 'agent-architecture',

    'workflow-os': 'workflow-automation',
    'workflow-systems': 'workflow-automation',
    'workflows': 'workflow-automation',
    'workflow': 'workflow-automation',
    'automation': 'workflow-automation',
    'executable-protocols': 'workflow-automation',

    'constitutional': 'constitutional-driven-automation',
    'doctrine': 'constitutional-driven-automation',

    'architecture-design': 'system-design',
    'architecture': 'system-design',

    'validation': 'validation-testing',
    'testing': 'validation-testing',

    'git': 'git-version-control',
    'github': 'git-version-control',

    'data-extraction': 'data-engineering',
    'data-processing': 'data-engineering',

    'canonical': 'governance',
    'normalized': 'governance',
    'consistency': 'governance',
    'auditability': 'governance',
    'validity-boundaries': 'governance',

    'safety': 'security-safety',

    'cursor': 'commands',
    'kanban': 'jira-project-management',
    'testimonial-collector': 'business-marketing',
    'action-plan': 'knowledge-management',
}

# Tags that should be in reuse: not themes:
REUSE_TAGS = {
    'blog', 'book', 'consulting', 'training',
    'documentation', 'internal-ops', 'email'
}

# Deprecated themes to remove
DEPRECATED_THEMES = {
    'health-parasites', 'biofilms'  # Remove if <5 blocks
}


def parse_frontmatter(content: str) -> tuple:
    """Extract frontmatter and content from markdown file."""
    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    try:
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2]
        return frontmatter, body
    except:
        return None, content


def consolidate_themes(themes: List[str]) -> List[str]:
    """Consolidate themes using mapping."""
    consolidated = set()

    for theme in themes:
        # Skip if it's a reuse tag (will be moved to reuse field)
        if theme in REUSE_TAGS:
            continue

        # Skip deprecated themes
        if theme in DEPRECATED_THEMES:
            continue

        # Map to canonical theme
        canonical = THEME_CONSOLIDATION.get(theme, theme)
        consolidated.add(canonical)

    return sorted(list(consolidated))


def extract_reuse_tags(themes: List[str], existing_reuse: List[str] = None) -> List[str]:
    """Extract reuse tags from themes."""
    reuse = set(existing_reuse) if existing_reuse else set()

    for theme in themes:
        if theme in REUSE_TAGS:
            reuse.add(theme)

    return sorted(list(reuse))


def process_block(file_path: Path, dry_run: bool = True) -> dict:
    """Process a single block file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        frontmatter, body = parse_frontmatter(content)

        if not frontmatter:
            return {
                'status': 'skip',
                'reason': 'No frontmatter',
                'file': str(file_path)
            }

        # Get current themes
        old_themes = frontmatter.get('themes', [])
        if not old_themes:
            return {
                'status': 'skip',
                'reason': 'No themes',
                'file': str(file_path)
            }

        # Consolidate themes
        new_themes = consolidate_themes(old_themes)

        # Extract reuse tags
        existing_reuse = frontmatter.get('reuse', [])
        new_reuse = extract_reuse_tags(old_themes, existing_reuse)

        # Check if changes needed
        if new_themes == old_themes and new_reuse == existing_reuse:
            return {
                'status': 'unchanged',
                'file': str(file_path)
            }

        # Update frontmatter
        frontmatter['themes'] = new_themes
        if new_reuse:
            frontmatter['reuse'] = new_reuse

        # Write back if not dry run
        if not dry_run:
            new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)}---{body}"
            file_path.write_text(new_content, encoding='utf-8')

        return {
            'status': 'updated',
            'file': str(file_path),
            'old_themes': old_themes,
            'new_themes': new_themes,
            'new_reuse': new_reuse
        }

    except Exception as e:
        return {
            'status': 'error',
            'file': str(file_path),
            'error': str(e)
        }


def main():
    import argparse

    ap = argparse.ArgumentParser(
        description="Consolidate themes across all blocks"
    )
    ap.add_argument(
        '--blocks-dir',
        type=Path,
        default=Path('./blocks'),
        help='Path to blocks directory'
    )
    ap.add_argument(
        '--dry-run',
        action='store_true',
        help='Show changes without applying them'
    )

    args = ap.parse_args()

    if not args.blocks_dir.exists():
        print(f"ERROR: Blocks directory not found: {args.blocks_dir}")
        sys.exit(1)

    # Find all markdown files
    blocks = list(args.blocks_dir.rglob('*.md'))

    print(f"Found {len(blocks)} blocks")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'APPLY CHANGES'}")
    print()

    results = {
        'updated': [],
        'unchanged': [],
        'skip': [],
        'error': []
    }

    for block in blocks:
        result = process_block(block, dry_run=args.dry_run)
        status = result['status']
        results[status].append(result)

        if status == 'updated':
            print(f"✓ {block.relative_to(args.blocks_dir)}")
            print(f"  Old themes: {result['old_themes']}")
            print(f"  New themes: {result['new_themes']}")
            if result['new_reuse']:
                print(f"  Reuse tags: {result['new_reuse']}")
            print()
        elif status == 'error':
            print(f"✗ {block.relative_to(args.blocks_dir)}: {result['error']}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Updated:   {len(results['updated'])}")
    print(f"Unchanged: {len(results['unchanged'])}")
    print(f"Skipped:   {len(results['skip'])}")
    print(f"Errors:    {len(results['error'])}")

    if args.dry_run and results['updated']:
        print("\nTo apply changes, run without --dry-run flag")

    sys.exit(0 if not results['error'] else 1)


if __name__ == '__main__':
    main()

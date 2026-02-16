#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archive Theme Tagger

Auto-tags ChatGPT archive conversations with themes based on
chatgpt-archive-theme-taxonomy.md framework using keyword matching.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set
import yaml

# Theme taxonomy from chatgpt-archive-theme-taxonomy.md
THEME_KEYWORDS = {
    'translation-localization': [
        'translat', 'übersetzen', 'перевод', 'german', 'russian', 'english',
        'deutsch', 'русский', 'multilingual', 'language', 'localization'
    ],
    'ai-agents-automation': [
        'agent', 'ai', 'automation', 'chatgpt', 'openai', 'gpt', 'llm',
        'prompt', 'workflow', 'automat'
    ],
    'jira-project-management': [
        'jira', 'project', 'management', 'scrum', 'kanban', 'task',
        'issue', 'ticket', 'sprint', 'agile'
    ],
    'huna-spirituality-wellness': [
        'huna', 'meditation', 'spiritual', 'goddess', 'chakra',
        'healing', 'wellness', 'energy', 'ho oponopono'
    ],
    'music-audio-production': [
        'music', 'song', 'album', 'audio', 'cover', 'elevenlabs',
        'voice', 'sound', 'песня', 'музык'
    ],
    'technical-development': [
        'github', 'python', 'javascript', 'api', 'aws', 'docker',
        'development', 'code', 'programming', 'git', 'database'
    ],
    'content-writing-email': [
        'content', 'writing', 'blog', 'article', 'copy', 'email',
        'text', 'write', 'draft'
    ],
    'design-creative': [
        'design', 'creative', 'graphic', 'visual', 'ui', 'ux',
        'cover', 'logo', 'branding'
    ],
    'business-marketing': [
        'business', 'marketing', 'strategy', 'market', 'sales',
        'commercial', 'acquisition', 'revenue'
    ],
    'german-language-admin': [
        'lexoffice', 'steuererklärung', 'finanzamt', 'steuer',
        'buchung', 'german admin', 'verwaltung'
    ],
    'workflow-productivity': [
        'workflow', 'productivity', 'efficiency', 'optimization',
        'process', 'improvement'
    ],
    'data-extraction-pdf': [
        'pdf', 'extract', 'extraction', 'parse', 'ocr',
        'document', 'data extraction', 'text recognition'
    ],
}

def parse_frontmatter(content: str) -> tuple:
    """Extract frontmatter and content from markdown file."""
    # Archive format: # Title\n\n```yaml\n...\n```\n---\n...
    # Find yaml block
    if '```yaml' not in content:
        return None, content

    parts = content.split('```', 2)
    if len(parts) < 3:
        return None, content

    try:
        # Extract title (before yaml block)
        title_part = parts[0]

        # Parse YAML block
        yaml_content = parts[1].replace('yaml\n', '', 1)  # Remove 'yaml' marker
        frontmatter = yaml.safe_load(yaml_content)

        # Rest of content
        body = parts[2]

        return frontmatter, title_part + body
    except Exception as e:
        return None, content


def classify_by_keywords(title: str, content: str, max_themes: int = 3) -> List[str]:
    """Classify content by keyword matching."""
    # Combine title and first 1000 chars of content
    search_text = (title + ' ' + content[:1000]).lower()

    # Score each theme
    theme_scores = {}
    for theme, keywords in THEME_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Count keyword occurrences (case-insensitive)
            count = len(re.findall(r'\b' + re.escape(keyword), search_text, re.IGNORECASE))
            score += count

        if score > 0:
            theme_scores[theme] = score

    # Return top N themes
    sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
    return [theme for theme, score in sorted_themes[:max_themes]]


def extract_title_from_filename(filename: str) -> str:
    """Extract human-readable title from filename."""
    # Remove UUID suffix
    name = re.sub(r'__[0-9a-f-]+\.md$', '', filename)
    # Replace dashes/underscores with spaces
    name = name.replace('-', ' ').replace('_', ' ')
    return name


def tag_conversation(file_path: Path, dry_run: bool = True) -> dict:
    """Tag a single conversation file with themes."""
    try:
        content = file_path.read_text(encoding='utf-8')
        frontmatter, body = parse_frontmatter(content)

        if not frontmatter:
            return {
                'status': 'skip',
                'reason': 'No frontmatter',
                'file': str(file_path)
            }

        # Skip if already has themes (non-empty list)
        existing_themes = frontmatter.get('themes', [])
        if existing_themes and len(existing_themes) > 0:
            return {
                'status': 'skip',
                'reason': 'Already tagged',
                'file': str(file_path),
                'existing_themes': existing_themes
            }

        # Extract title from filename or frontmatter
        title = extract_title_from_filename(file_path.name)

        # Classify by keywords
        themes = classify_by_keywords(title, body)

        if not themes:
            return {
                'status': 'skip',
                'reason': 'No themes matched',
                'file': str(file_path)
            }

        # Add themes to frontmatter
        frontmatter['themes'] = themes

        # Write back if not dry run
        if not dry_run:
            # Reconstruct file with updated frontmatter
            yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
            new_content = f"```yaml\n{yaml_str}```{body}"
            file_path.write_text(new_content, encoding='utf-8')

        return {
            'status': 'tagged',
            'file': str(file_path),
            'themes': themes,
            'title': title
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
        description="Tag ChatGPT archive conversations with themes"
    )
    ap.add_argument(
        '--archive-dir',
        type=Path,
        default=Path('./import/normalized'),
        help='Path to archive directory'
    )
    ap.add_argument(
        '--dry-run',
        action='store_true',
        help='Show changes without applying them'
    )
    ap.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of files to process (for testing)'
    )
    ap.add_argument(
        '--stats-only',
        action='store_true',
        help='Only show statistics without processing'
    )

    args = ap.parse_args()

    if not args.archive_dir.exists():
        print(f"ERROR: Archive directory not found: {args.archive_dir}")
        sys.exit(1)

    # Find all markdown files
    conversations = list(args.archive_dir.glob('*.md'))

    print(f"Found {len(conversations)} conversations")

    if args.stats_only:
        # Count by existing themes
        theme_counts = {}
        for conv in conversations:
            try:
                content = conv.read_text(encoding='utf-8')
                fm, _ = parse_frontmatter(content)
                if fm and fm.get('themes'):
                    for theme in fm['themes']:
                        theme_counts[theme] = theme_counts.get(theme, 0) + 1
            except:
                pass

        print(f"\nExisting theme distribution:")
        for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {theme}: {count}")
        sys.exit(0)

    print(f"Mode: {'DRY RUN' if args.dry_run else 'APPLY CHANGES'}")

    if args.limit:
        print(f"Limiting to {args.limit} files\n")
        conversations = conversations[:args.limit]

    results = {
        'tagged': [],
        'skip': [],
        'error': []
    }

    for i, conv in enumerate(conversations, 1):
        if i % 100 == 0:
            print(f"Processing {i}/{len(conversations)}...")

        result = tag_conversation(conv, dry_run=args.dry_run)
        status = result['status']
        results[status].append(result)

        if status == 'tagged':
            print(f"✓ {conv.name}")
            print(f"  Themes: {', '.join(result['themes'])}")
        elif status == 'error':
            print(f"✗ {conv.name}: {result['error']}")

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Tagged:  {len(results['tagged'])}")
    print(f"Skipped: {len(results['skip'])}")
    print(f"Errors:  {len(results['error'])}")

    # Theme distribution
    if results['tagged']:
        theme_counts = {}
        for r in results['tagged']:
            for theme in r['themes']:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1

        print(f"\nTheme distribution (new tags):")
        for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {theme}: {count}")

    if args.dry_run and results['tagged']:
        print("\nTo apply changes, run without --dry-run flag")

    sys.exit(0 if not results['error'] else 1)


if __name__ == '__main__':
    main()

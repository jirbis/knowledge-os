#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read_block.py - Read a single block with metadata from knowledge-os.

Usage:
    python3 tools/read_block.py <block_id> [--output json|yaml|markdown]
    python3 tools/read_block.py --path <file_path>
    python3 tools/read_block.py --list [--type <type>]

Options:
    block_id        Block ID (e.g., frameworks.marketing-funnel-project-framework)
    --path, -p      Read by file path instead of block ID
    --output, -o    Output format: json, yaml, or markdown (default: markdown)
    --list, -l      List all available blocks
    --type, -t      Filter by type when listing
    --blocks-dir    Path to blocks directory (default: ./blocks)
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class Block:
    """A knowledge block with content and metadata."""
    block_id: str
    path: str
    title: str
    type: str
    content: str
    frontmatter: dict
    modified: str
    word_count: int
    line_count: int


def extract_yaml_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                if YAML_AVAILABLE:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                else:
                    # Simple fallback parser
                    frontmatter = {}
                    for line in parts[1].strip().split('\n'):
                        if ':' in line:
                            key, val = line.split(':', 1)
                            frontmatter[key.strip()] = val.strip()
                body = parts[2].strip()
                return frontmatter, body
            except Exception:
                pass
    return {}, content


def block_id_to_path(block_id: str, blocks_dir: Path) -> Optional[Path]:
    """Convert block ID to file path."""
    # block_id format: type.name or type.subdir.name
    # e.g., frameworks.marketing-funnel-project-framework
    parts = block_id.split('.')
    rel_path = '/'.join(parts) + '.md'
    full_path = blocks_dir / rel_path

    if full_path.exists():
        return full_path

    # Try with hyphens as directory separators
    for i in range(1, len(parts)):
        alt_path = blocks_dir / '/'.join(parts[:i]) / ('-'.join(parts[i:]) + '.md')
        if alt_path.exists():
            return alt_path

    return None


def path_to_block_id(path: Path, blocks_dir: Path) -> str:
    """Convert file path to block ID."""
    rel_path = path.relative_to(blocks_dir)
    block_id = str(rel_path).replace('/', '.').replace('\\', '.').removesuffix('.md')
    return block_id


def read_block(path: Path, blocks_dir: Path) -> Block:
    """Read a block from file."""
    content = path.read_text(encoding='utf-8')
    frontmatter, body = extract_yaml_frontmatter(content)

    rel_path = path.relative_to(blocks_dir)
    block_type = rel_path.parts[0] if rel_path.parts else 'unknown'

    return Block(
        block_id=path_to_block_id(path, blocks_dir),
        path=str(path),
        title=frontmatter.get('title', path.stem.replace('-', ' ').title()),
        type=block_type,
        content=body,
        frontmatter=frontmatter,
        modified=datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
        word_count=len(body.split()),
        line_count=len(body.split('\n')),
    )


def list_blocks(blocks_dir: Path, block_type: Optional[str] = None) -> list[dict]:
    """List all blocks in the directory."""
    blocks = []

    for md_file in blocks_dir.rglob('*.md'):
        # Skip hidden and special files
        if md_file.name.startswith('.') or md_file.name.startswith('_'):
            continue

        rel_path = md_file.relative_to(blocks_dir)
        file_type = rel_path.parts[0] if rel_path.parts else 'unknown'

        if block_type and file_type != block_type:
            continue

        content = md_file.read_text(encoding='utf-8')
        frontmatter, body = extract_yaml_frontmatter(content)

        blocks.append({
            'block_id': path_to_block_id(md_file, blocks_dir),
            'path': str(md_file),
            'title': frontmatter.get('title', md_file.stem.replace('-', ' ').title()),
            'type': file_type,
            'word_count': len(body.split()),
        })

    return sorted(blocks, key=lambda b: (b['type'], b['block_id']))


def format_block_markdown(block: Block) -> str:
    """Format block as markdown."""
    lines = [
        f"# {block.title}",
        "",
        f"**Block ID:** `{block.block_id}`",
        f"**Type:** {block.type}",
        f"**Path:** `{block.path}`",
        f"**Modified:** {block.modified}",
        f"**Words:** {block.word_count} | **Lines:** {block.line_count}",
        "",
    ]

    if block.frontmatter:
        lines.append("## Frontmatter")
        lines.append("```yaml")
        if YAML_AVAILABLE:
            lines.append(yaml.dump(block.frontmatter, default_flow_style=False).strip())
        else:
            lines.append(json.dumps(block.frontmatter, indent=2))
        lines.append("```")
        lines.append("")

    lines.append("## Content")
    lines.append("")
    lines.append(block.content)

    return '\n'.join(lines)


def format_block_json(block: Block) -> str:
    """Format block as JSON."""
    return json.dumps(asdict(block), indent=2)


def format_block_yaml(block: Block) -> str:
    """Format block as YAML."""
    if not YAML_AVAILABLE:
        return "Error: PyYAML not installed. Use --output json instead."
    return yaml.dump(asdict(block), default_flow_style=False, allow_unicode=True)


def format_list_text(blocks: list[dict]) -> str:
    """Format block list as text."""
    if not blocks:
        return "No blocks found."

    lines = [f"Found {len(blocks)} blocks:\n"]

    current_type = None
    for b in blocks:
        if b['type'] != current_type:
            current_type = b['type']
            lines.append(f"\n## {current_type}/")

        lines.append(f"  - {b['block_id']} ({b['word_count']} words)")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Read knowledge-os blocks")
    parser.add_argument("block_id", nargs='?', help="Block ID to read")
    parser.add_argument("--path", "-p", type=Path, help="Read by file path")
    parser.add_argument("--output", "-o", choices=["json", "yaml", "markdown"],
                        default="markdown", help="Output format")
    parser.add_argument("--list", "-l", action="store_true", help="List all blocks")
    parser.add_argument("--type", "-t", dest="block_type", help="Filter by type")
    parser.add_argument("--blocks-dir", type=Path, default=Path("./blocks"),
                        help="Path to blocks directory")

    args = parser.parse_args()

    if not args.blocks_dir.exists():
        print(f"Error: Blocks directory not found: {args.blocks_dir}", file=sys.stderr)
        return 1

    # List mode
    if args.list:
        blocks = list_blocks(args.blocks_dir, args.block_type)
        if args.output == "json":
            print(json.dumps(blocks, indent=2))
        elif args.output == "yaml" and YAML_AVAILABLE:
            print(yaml.dump(blocks, default_flow_style=False))
        else:
            print(format_list_text(blocks))
        return 0

    # Read mode - need block_id or path
    if not args.block_id and not args.path:
        parser.print_help()
        return 1

    # Determine file path
    if args.path:
        file_path = args.path
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            return 1
    else:
        file_path = block_id_to_path(args.block_id, args.blocks_dir)
        if not file_path:
            print(f"Error: Block not found: {args.block_id}", file=sys.stderr)
            print(f"Searched in: {args.blocks_dir}", file=sys.stderr)
            return 1

    # Read and format block
    try:
        block = read_block(file_path, args.blocks_dir)

        if args.output == "json":
            print(format_block_json(block))
        elif args.output == "yaml":
            print(format_block_yaml(block))
        else:
            print(format_block_markdown(block))

        return 0

    except Exception as e:
        print(f"Error reading block: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    exit(main())

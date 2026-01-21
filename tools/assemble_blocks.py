#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
assemble_blocks.py - Combine multiple blocks into a single output document.

Usage:
    python3 tools/assemble_blocks.py --blocks <block_ids...> --output <output.md>
    python3 tools/assemble_blocks.py --query "marketing funnel" --output <output.md>

Options:
    --blocks, -b    Block IDs to assemble (space-separated)
    --query, -q     Search query to find blocks to assemble
    --output, -o    Output file path (required)
    --format, -f    Output format: markdown, json (default: markdown)
    --title         Title for assembled document
    --limit, -n     Max blocks when using query (default: 5)
    --blocks-dir    Path to blocks directory (default: ./blocks)
    --db            Embeddings database for query mode (default: ./index/embeddings.sqlite)
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Import local modules
from read_block import read_block, block_id_to_path, Block


def assemble_markdown(
    blocks: list[Block],
    title: str,
    include_metadata: bool = True,
) -> str:
    """Assemble blocks into a markdown document."""
    lines = []

    # Frontmatter
    lines.append("---")
    lines.append(f"title: \"{title}\"")
    lines.append(f"type: assembled")
    lines.append(f"created: \"{datetime.now().isoformat()}\"")
    lines.append(f"source_blocks:")
    for b in blocks:
        lines.append(f"  - {b.block_id}")
    lines.append("status: draft")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# {title}")
    lines.append("")

    # Table of contents
    if len(blocks) > 1:
        lines.append("## Contents")
        lines.append("")
        for i, b in enumerate(blocks, 1):
            anchor = b.title.lower().replace(' ', '-').replace(':', '')
            lines.append(f"{i}. [{b.title}](#{anchor})")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Assembled content
    for i, block in enumerate(blocks):
        lines.append(f"## {block.title}")
        lines.append("")

        if include_metadata:
            lines.append(f"> **Source:** `{block.block_id}` | **Type:** {block.type}")
            lines.append("")

        lines.append(block.content)
        lines.append("")

        if i < len(blocks) - 1:
            lines.append("---")
            lines.append("")

    # References
    lines.append("## References")
    lines.append("")
    for b in blocks:
        lines.append(f"- `{b.block_id}`: {b.title} ({b.word_count} words)")
    lines.append("")

    return '\n'.join(lines)


def assemble_json(blocks: list[Block], title: str) -> str:
    """Assemble blocks into JSON format."""
    data = {
        "title": title,
        "type": "assembled",
        "created": datetime.now().isoformat(),
        "source_blocks": [b.block_id for b in blocks],
        "blocks": [
            {
                "block_id": b.block_id,
                "title": b.title,
                "type": b.type,
                "content": b.content,
                "word_count": b.word_count,
            }
            for b in blocks
        ],
        "total_words": sum(b.word_count for b in blocks),
    }
    return json.dumps(data, indent=2)


def search_blocks_for_assembly(
    query: str,
    db_path: Path,
    limit: int = 5,
) -> list[str]:
    """Search for blocks and return block IDs."""
    try:
        from semantic_search import SemanticSearcher
        searcher = SemanticSearcher(db_path)
        results = searcher.search(query, limit=limit)
        searcher.close()

        # Deduplicate by block_id (multiple chunks per block)
        seen = set()
        block_ids = []
        for r in results:
            if r.block_id not in seen:
                seen.add(r.block_id)
                block_ids.append(r.block_id)

        return block_ids
    except Exception as e:
        print(f"Warning: Semantic search failed: {e}")
        return []


def load_blocks(
    block_ids: list[str],
    blocks_dir: Path,
) -> list[Block]:
    """Load blocks by their IDs."""
    blocks = []

    for block_id in block_ids:
        path = block_id_to_path(block_id, blocks_dir)
        if path:
            try:
                block = read_block(path, blocks_dir)
                blocks.append(block)
            except Exception as e:
                print(f"Warning: Could not read block {block_id}: {e}")
        else:
            print(f"Warning: Block not found: {block_id}")

    return blocks


def main():
    parser = argparse.ArgumentParser(description="Assemble knowledge-os blocks")
    parser.add_argument("--blocks", "-b", nargs="+", help="Block IDs to assemble")
    parser.add_argument("--query", "-q", help="Search query to find blocks")
    parser.add_argument("--output", "-o", type=Path, required=True,
                        help="Output file path")
    parser.add_argument("--format", "-f", choices=["markdown", "json"],
                        default="markdown", help="Output format")
    parser.add_argument("--title", default="Assembled Document",
                        help="Title for assembled document")
    parser.add_argument("--limit", "-n", type=int, default=5,
                        help="Max blocks when using query")
    parser.add_argument("--blocks-dir", type=Path, default=Path("./blocks"),
                        help="Path to blocks directory")
    parser.add_argument("--db", type=Path, default=Path("./index/embeddings.sqlite"),
                        help="Embeddings database path")
    parser.add_argument("--no-metadata", action="store_true",
                        help="Don't include source metadata in output")

    args = parser.parse_args()

    if not args.blocks and not args.query:
        print("Error: Either --blocks or --query is required")
        return 1

    if not args.blocks_dir.exists():
        print(f"Error: Blocks directory not found: {args.blocks_dir}")
        return 1

    # Get block IDs
    if args.query:
        print(f"Searching for: {args.query}")
        block_ids = search_blocks_for_assembly(args.query, args.db, args.limit)
        if not block_ids:
            print("No blocks found for query.")
            return 1
        print(f"Found {len(block_ids)} blocks: {', '.join(block_ids)}")
    else:
        block_ids = args.blocks

    # Load blocks
    blocks = load_blocks(block_ids, args.blocks_dir)

    if not blocks:
        print("Error: No blocks could be loaded")
        return 1

    print(f"Assembling {len(blocks)} blocks...")

    # Generate output
    if args.format == "markdown":
        content = assemble_markdown(
            blocks,
            args.title,
            include_metadata=not args.no_metadata,
        )
    else:
        content = assemble_json(blocks, args.title)

    # Write output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding='utf-8')

    total_words = sum(b.word_count for b in blocks)
    print(f"Assembled document written to: {args.output}")
    print(f"Total: {len(blocks)} blocks, {total_words} words")

    return 0


if __name__ == "__main__":
    exit(main())

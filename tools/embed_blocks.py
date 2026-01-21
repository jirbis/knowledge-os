#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
embed_blocks.py - Generate embeddings for all knowledge-os blocks.

Usage:
    python3 tools/embed_blocks.py [--blocks-dir BLOCKS_DIR] [--output OUTPUT] [--model MODEL]

Options:
    --blocks-dir    Path to blocks directory (default: ./blocks)
    --output        Output SQLite database (default: ./index/embeddings.sqlite)
    --model         Embedding model: openai or local (default: openai)
    --chunk-size    Chunk size in tokens (default: 512)
    --overlap       Chunk overlap in tokens (default: 64)
    --force         Force re-embedding of all blocks
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional

# Try to import embedding libraries
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    LOCAL_AVAILABLE = True
except ImportError:
    LOCAL_AVAILABLE = False


@dataclass
class BlockChunk:
    """A chunk of a block for embedding."""
    block_id: str
    block_path: str
    chunk_index: int
    content: str
    metadata: dict


@dataclass
class EmbeddedChunk:
    """A chunk with its embedding."""
    block_id: str
    block_path: str
    chunk_index: int
    content: str
    embedding: list[float]
    metadata: dict
    content_hash: str


def extract_yaml_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from markdown content."""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                import yaml
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
                return frontmatter, body
            except Exception:
                pass
    return {}, content


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Split text into overlapping chunks by approximate token count."""
    # Rough approximation: 1 token ≈ 4 characters
    char_chunk_size = chunk_size * 4
    char_overlap = overlap * 4

    if len(text) <= char_chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + char_chunk_size

        # Try to break at paragraph or sentence boundary
        if end < len(text):
            # Look for paragraph break
            para_break = text.rfind('\n\n', start + char_overlap, end)
            if para_break > start + char_overlap:
                end = para_break
            else:
                # Look for sentence break
                sentence_break = max(
                    text.rfind('. ', start + char_overlap, end),
                    text.rfind('.\n', start + char_overlap, end),
                )
                if sentence_break > start + char_overlap:
                    end = sentence_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - char_overlap if end < len(text) else len(text)

    return chunks


def iter_blocks(blocks_dir: Path) -> Iterator[tuple[str, str, dict]]:
    """Iterate over all markdown blocks in the blocks directory."""
    for md_file in blocks_dir.rglob('*.md'):
        # Skip hidden files and special files
        if md_file.name.startswith('.') or md_file.name.startswith('_'):
            continue

        # Generate block ID from relative path
        rel_path = md_file.relative_to(blocks_dir)
        block_id = str(rel_path).replace('/', '.').replace('\\', '.').removesuffix('.md')

        content = md_file.read_text(encoding='utf-8')
        frontmatter, body = extract_yaml_frontmatter(content)

        metadata = {
            'path': str(md_file),
            'relative_path': str(rel_path),
            'type': rel_path.parts[0] if rel_path.parts else 'unknown',
            'title': frontmatter.get('title', md_file.stem),
            'tags': frontmatter.get('tags', []),
            'modified': datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
        }
        metadata.update(frontmatter)

        yield block_id, body, metadata


def create_chunks(blocks_dir: Path, chunk_size: int, overlap: int) -> Iterator[BlockChunk]:
    """Create chunks from all blocks."""
    for block_id, content, metadata in iter_blocks(blocks_dir):
        chunks = chunk_text(content, chunk_size, overlap)
        for i, chunk_content in enumerate(chunks):
            yield BlockChunk(
                block_id=block_id,
                block_path=metadata['path'],
                chunk_index=i,
                content=chunk_content,
                metadata=metadata,
            )


class OpenAIEmbedder:
    """Embed text using OpenAI API."""

    def __init__(self, model: str = "text-embedding-3-small"):
        if not OPENAI_AVAILABLE:
            raise RuntimeError("openai package not installed. Run: pip install openai")
        self.client = openai.OpenAI()
        self.model = model

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts."""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]

    @property
    def dimension(self) -> int:
        return 1536 if 'small' in self.model else 3072


class LocalEmbedder:
    """Embed text using local sentence-transformers model."""

    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        if not LOCAL_AVAILABLE:
            raise RuntimeError("sentence-transformers not installed. Run: pip install sentence-transformers")
        self.model = SentenceTransformer(model)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return [emb.tolist() for emb in embeddings]

    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()


def init_database(db_path: Path, dimension: int) -> sqlite3.Connection:
    """Initialize SQLite database for embeddings."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            block_id TEXT NOT NULL,
            block_path TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            embedding BLOB NOT NULL,
            metadata TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(block_id, chunk_index)
        );

        CREATE INDEX IF NOT EXISTS idx_block_id ON embeddings(block_id);
        CREATE INDEX IF NOT EXISTS idx_content_hash ON embeddings(content_hash);

        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
    """)

    # Store dimension
    conn.execute(
        "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
        ("dimension", str(dimension))
    )
    conn.commit()

    return conn


def content_hash(content: str) -> str:
    """Generate hash of content for change detection."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def needs_update(conn: sqlite3.Connection, block_id: str, chunk_index: int, new_hash: str) -> bool:
    """Check if a chunk needs to be re-embedded."""
    row = conn.execute(
        "SELECT content_hash FROM embeddings WHERE block_id = ? AND chunk_index = ?",
        (block_id, chunk_index)
    ).fetchone()

    if row is None:
        return True
    return row['content_hash'] != new_hash


def store_embedding(conn: sqlite3.Connection, chunk: EmbeddedChunk):
    """Store an embedded chunk in the database."""
    import struct

    # Pack embedding as binary blob (more efficient than JSON)
    embedding_blob = struct.pack(f'{len(chunk.embedding)}f', *chunk.embedding)

    conn.execute("""
        INSERT OR REPLACE INTO embeddings
        (block_id, block_path, chunk_index, content, content_hash, embedding, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        chunk.block_id,
        chunk.block_path,
        chunk.chunk_index,
        chunk.content,
        chunk.content_hash,
        embedding_blob,
        json.dumps(chunk.metadata),
        datetime.now().isoformat(),
    ))


def embed_blocks(
    blocks_dir: Path,
    output_path: Path,
    model: str = "openai",
    chunk_size: int = 512,
    overlap: int = 64,
    force: bool = False,
    batch_size: int = 100,
) -> dict:
    """Embed all blocks and store in SQLite database."""

    # Initialize embedder
    if model == "openai":
        embedder = OpenAIEmbedder()
    elif model == "local":
        embedder = LocalEmbedder()
    else:
        raise ValueError(f"Unknown model: {model}. Use 'openai' or 'local'")

    # Initialize database
    conn = init_database(output_path, embedder.dimension)

    stats = {
        'total_blocks': 0,
        'total_chunks': 0,
        'embedded': 0,
        'skipped': 0,
        'errors': 0,
    }

    # Collect chunks that need embedding
    chunks_to_embed: list[BlockChunk] = []
    seen_blocks = set()

    for chunk in create_chunks(blocks_dir, chunk_size, overlap):
        stats['total_chunks'] += 1
        seen_blocks.add(chunk.block_id)

        chunk_hash = content_hash(chunk.content)

        if force or needs_update(conn, chunk.block_id, chunk.chunk_index, chunk_hash):
            chunk.metadata['content_hash'] = chunk_hash
            chunks_to_embed.append(chunk)
        else:
            stats['skipped'] += 1

    stats['total_blocks'] = len(seen_blocks)

    # Embed in batches
    for i in range(0, len(chunks_to_embed), batch_size):
        batch = chunks_to_embed[i:i + batch_size]
        texts = [c.content for c in batch]

        try:
            embeddings = embedder.embed(texts)

            for chunk, embedding in zip(batch, embeddings):
                embedded = EmbeddedChunk(
                    block_id=chunk.block_id,
                    block_path=chunk.block_path,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    embedding=embedding,
                    metadata=chunk.metadata,
                    content_hash=chunk.metadata['content_hash'],
                )
                store_embedding(conn, embedded)
                stats['embedded'] += 1

            conn.commit()
            print(f"Embedded batch {i // batch_size + 1}: {len(batch)} chunks")

        except Exception as e:
            print(f"Error embedding batch: {e}")
            stats['errors'] += len(batch)

    # Clean up old chunks for blocks that no longer exist
    conn.execute("""
        DELETE FROM embeddings
        WHERE block_id NOT IN ({})
    """.format(','.join('?' * len(seen_blocks))), list(seen_blocks))
    conn.commit()

    conn.close()
    return stats


def main():
    parser = argparse.ArgumentParser(description="Embed knowledge-os blocks for semantic search")
    parser.add_argument("--blocks-dir", type=Path, default=Path("./blocks"),
                        help="Path to blocks directory")
    parser.add_argument("--output", type=Path, default=Path("./index/embeddings.sqlite"),
                        help="Output SQLite database path")
    parser.add_argument("--model", choices=["openai", "local"], default="openai",
                        help="Embedding model to use")
    parser.add_argument("--chunk-size", type=int, default=512,
                        help="Chunk size in tokens")
    parser.add_argument("--overlap", type=int, default=64,
                        help="Chunk overlap in tokens")
    parser.add_argument("--force", action="store_true",
                        help="Force re-embedding of all blocks")

    args = parser.parse_args()

    if not args.blocks_dir.exists():
        print(f"Error: Blocks directory not found: {args.blocks_dir}")
        return 1

    print(f"Embedding blocks from: {args.blocks_dir}")
    print(f"Output: {args.output}")
    print(f"Model: {args.model}")
    print(f"Chunk size: {args.chunk_size}, Overlap: {args.overlap}")
    print()

    stats = embed_blocks(
        blocks_dir=args.blocks_dir,
        output_path=args.output,
        model=args.model,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        force=args.force,
    )

    print()
    print("=== Embedding Complete ===")
    print(f"Total blocks: {stats['total_blocks']}")
    print(f"Total chunks: {stats['total_chunks']}")
    print(f"Embedded: {stats['embedded']}")
    print(f"Skipped (unchanged): {stats['skipped']}")
    print(f"Errors: {stats['errors']}")

    return 0


if __name__ == "__main__":
    exit(main())

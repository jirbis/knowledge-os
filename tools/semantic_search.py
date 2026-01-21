#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
semantic_search.py - Query embeddings for semantic search over knowledge-os blocks.

Usage:
    python3 tools/semantic_search.py --query "marketing funnel" [--limit 10] [--type frameworks]

Options:
    --query, -q     Search query (required)
    --db            Embeddings database (default: ./index/embeddings.sqlite)
    --limit, -n     Maximum results (default: 10)
    --type, -t      Filter by block type (frameworks, checklists, plans, narratives, etc.)
    --threshold     Minimum similarity score 0-1 (default: 0.3)
    --output, -o    Output format: text, json, or markdown (default: text)
    --fallback      Use FTS5 fallback if embeddings unavailable
"""

import argparse
import json
import sqlite3
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

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

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


@dataclass
class SearchResult:
    """A search result with similarity score."""
    block_id: str
    block_path: str
    chunk_index: int
    content: str
    similarity: float
    metadata: dict


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    if NUMPY_AVAILABLE:
        a_np = np.array(a)
        b_np = np.array(b)
        return float(np.dot(a_np, b_np) / (np.linalg.norm(a_np) * np.linalg.norm(b_np)))
    else:
        # Pure Python fallback
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def get_embedding_dimension(conn: sqlite3.Connection) -> int:
    """Get embedding dimension from database metadata."""
    row = conn.execute("SELECT value FROM metadata WHERE key = 'dimension'").fetchone()
    return int(row[0]) if row else 1536


def unpack_embedding(blob: bytes, dimension: int) -> list[float]:
    """Unpack embedding from binary blob."""
    return list(struct.unpack(f'{dimension}f', blob))


class SemanticSearcher:
    """Semantic search over embedded blocks."""

    def __init__(self, db_path: Path, model: str = "openai"):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.dimension = get_embedding_dimension(self.conn)

        # Initialize embedder for query embedding
        if model == "openai":
            if not OPENAI_AVAILABLE:
                raise RuntimeError("openai package not installed")
            self.client = openai.OpenAI()
            self.model = "text-embedding-3-small"
            self._embed = self._embed_openai
        elif model == "local":
            if not LOCAL_AVAILABLE:
                raise RuntimeError("sentence-transformers not installed")
            self.transformer = SentenceTransformer("all-MiniLM-L6-v2")
            self._embed = self._embed_local
        else:
            raise ValueError(f"Unknown model: {model}")

    def _embed_openai(self, text: str) -> list[float]:
        """Embed query using OpenAI."""
        response = self.client.embeddings.create(
            model=self.model,
            input=[text],
        )
        return response.data[0].embedding

    def _embed_local(self, text: str) -> list[float]:
        """Embed query using local model."""
        embedding = self.transformer.encode([text], convert_to_numpy=True)
        return embedding[0].tolist()

    def search(
        self,
        query: str,
        limit: int = 10,
        block_type: Optional[str] = None,
        threshold: float = 0.3,
    ) -> list[SearchResult]:
        """Search for blocks similar to query."""

        # Embed the query
        query_embedding = self._embed(query)

        # Build SQL query with optional type filter
        sql = "SELECT block_id, block_path, chunk_index, content, embedding, metadata FROM embeddings"
        params = []

        if block_type:
            sql += " WHERE json_extract(metadata, '$.type') = ?"
            params.append(block_type)

        rows = self.conn.execute(sql, params).fetchall()

        # Calculate similarities
        results = []
        for row in rows:
            embedding = unpack_embedding(row['embedding'], self.dimension)
            similarity = cosine_similarity(query_embedding, embedding)

            if similarity >= threshold:
                results.append(SearchResult(
                    block_id=row['block_id'],
                    block_path=row['block_path'],
                    chunk_index=row['chunk_index'],
                    content=row['content'],
                    similarity=similarity,
                    metadata=json.loads(row['metadata']),
                ))

        # Sort by similarity and limit
        results.sort(key=lambda r: r.similarity, reverse=True)
        return results[:limit]

    def search_by_block_id(self, block_id: str) -> list[SearchResult]:
        """Get all chunks for a specific block."""
        rows = self.conn.execute(
            "SELECT block_id, block_path, chunk_index, content, metadata FROM embeddings WHERE block_id = ? ORDER BY chunk_index",
            (block_id,)
        ).fetchall()

        return [
            SearchResult(
                block_id=row['block_id'],
                block_path=row['block_path'],
                chunk_index=row['chunk_index'],
                content=row['content'],
                similarity=1.0,
                metadata=json.loads(row['metadata']),
            )
            for row in rows
        ]

    def list_blocks(self, block_type: Optional[str] = None) -> list[dict]:
        """List all unique blocks."""
        sql = """
            SELECT DISTINCT block_id, block_path, metadata
            FROM embeddings
            WHERE chunk_index = 0
        """
        params = []

        if block_type:
            sql = """
                SELECT DISTINCT block_id, block_path, metadata
                FROM embeddings
                WHERE chunk_index = 0 AND json_extract(metadata, '$.type') = ?
            """
            params.append(block_type)

        rows = self.conn.execute(sql, params).fetchall()
        return [
            {
                'block_id': row['block_id'],
                'block_path': row['block_path'],
                'metadata': json.loads(row['metadata']),
            }
            for row in rows
        ]

    def close(self):
        """Close database connection."""
        self.conn.close()


class FTS5Fallback:
    """FTS5 keyword search fallback when embeddings unavailable."""

    def __init__(self, db_path: Path):
        """Initialize with chat archive database."""
        self.db_path = db_path
        if not db_path.exists():
            raise FileNotFoundError(f"FTS5 database not found: {db_path}")
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row

    def search(self, query: str, limit: int = 10) -> list[dict]:
        """Search using FTS5."""
        sql = """
            SELECT
                m.conversation_id,
                c.title,
                m.role,
                snippet(messages_fts, 3, '[', ']', '…', 20) AS snippet,
                bm25(messages_fts) AS rank
            FROM messages_fts m
            JOIN conversations c ON c.id = m.conversation_id
            WHERE messages_fts MATCH ?
            ORDER BY rank
            LIMIT ?;
        """
        rows = self.conn.execute(sql, (query, limit)).fetchall()
        return [dict(row) for row in rows]

    def close(self):
        self.conn.close()


def format_results_text(results: list[SearchResult]) -> str:
    """Format results as plain text."""
    lines = []
    for i, r in enumerate(results, 1):
        lines.append(f"\n[{i}] {r.block_id} (score: {r.similarity:.3f})")
        lines.append(f"    Path: {r.block_path}")
        lines.append(f"    Type: {r.metadata.get('type', 'unknown')}")
        # Truncate content preview
        preview = r.content[:200].replace('\n', ' ')
        if len(r.content) > 200:
            preview += '...'
        lines.append(f"    Preview: {preview}")
    return '\n'.join(lines)


def format_results_json(results: list[SearchResult]) -> str:
    """Format results as JSON."""
    data = [
        {
            'block_id': r.block_id,
            'block_path': r.block_path,
            'chunk_index': r.chunk_index,
            'similarity': r.similarity,
            'content': r.content,
            'metadata': r.metadata,
        }
        for r in results
    ]
    return json.dumps(data, indent=2)


def format_results_markdown(results: list[SearchResult]) -> str:
    """Format results as markdown."""
    lines = ["# Search Results\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. {r.block_id}")
        lines.append(f"**Score:** {r.similarity:.3f} | **Type:** {r.metadata.get('type', 'unknown')}")
        lines.append(f"**Path:** `{r.block_path}`\n")
        lines.append("### Preview")
        lines.append(f"```\n{r.content[:500]}{'...' if len(r.content) > 500 else ''}\n```\n")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Semantic search over knowledge-os blocks")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--db", type=Path, default=Path("./index/embeddings.sqlite"),
                        help="Embeddings database path")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Maximum results")
    parser.add_argument("--type", "-t", dest="block_type", help="Filter by block type")
    parser.add_argument("--threshold", type=float, default=0.3,
                        help="Minimum similarity score (0-1)")
    parser.add_argument("--output", "-o", choices=["text", "json", "markdown"],
                        default="text", help="Output format")
    parser.add_argument("--model", choices=["openai", "local"], default="openai",
                        help="Embedding model for query")
    parser.add_argument("--fallback", type=Path, help="FTS5 database for fallback search")

    args = parser.parse_args()

    # Check if embeddings database exists
    if not args.db.exists():
        if args.fallback and args.fallback.exists():
            print(f"Embeddings not found. Using FTS5 fallback: {args.fallback}")
            searcher = FTS5Fallback(args.fallback)
            results = searcher.search(args.query, args.limit)
            print(json.dumps(results, indent=2))
            searcher.close()
            return 0
        else:
            print(f"Error: Embeddings database not found: {args.db}")
            print("Run embed_blocks.py first to generate embeddings.")
            return 1

    try:
        searcher = SemanticSearcher(args.db, model=args.model)
        results = searcher.search(
            query=args.query,
            limit=args.limit,
            block_type=args.block_type,
            threshold=args.threshold,
        )

        if not results:
            print("No results found.")
            return 0

        if args.output == "text":
            print(format_results_text(results))
        elif args.output == "json":
            print(format_results_json(results))
        elif args.output == "markdown":
            print(format_results_markdown(results))

        searcher.close()
        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

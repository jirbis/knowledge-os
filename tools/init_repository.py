#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository Initialization Script

Creates the required directory structure for Knowledge OS monorepo.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List


def create_directory_structure(base_path: Path, structure: List[str]) -> None:
    """Create directory structure"""
    for path_str in structure:
        path = base_path / path_str
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {path}")


def init_knowledge_os_repo(base_path: Path) -> None:
    """Initialize knowledge-os (main system) repository"""
    print(f"Initializing knowledge-os repository in {base_path}...")
    
    structure = [
        "blocks/conclusions",
        "blocks/frameworks",
        "blocks/checklists",
        "blocks/narratives",
        "blocks/metaphors",
        "blocks/plans",
        "export",
        "import/normalized",
        "index",
        "tools",
    ]
    
    create_directory_structure(base_path, structure)
    
    # Create minimal files
    (base_path / "README.md").touch(exist_ok=True)
    (base_path / "config.yaml").touch(exist_ok=True)
    
    print(f"✓ knowledge-os repository initialized")


def main():
    ap = argparse.ArgumentParser(
        description="Initialize Knowledge OS monorepo structure"
    )
    ap.add_argument(
        'path',
        type=Path,
        nargs='?',
        default=Path.cwd(),
        help="Base path for repository (default: current directory)"
    )
    
    args = ap.parse_args()
    
    if not args.path.exists():
        print(f"Creating directory: {args.path}")
        args.path.mkdir(parents=True, exist_ok=True)
    
    init_knowledge_os_repo(args.path)
    
    print("\n✓ Repository initialization complete")


if __name__ == "__main__":
    main()

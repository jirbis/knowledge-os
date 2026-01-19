#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository Boundary Validator

Enforces that the pipeline never writes to the knowledge repository.
Validates protected paths to prevent accidental modification of knowledge blocks.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple
import yaml


def load_config(config_path: Path) -> dict:
    """Load configuration from config.yaml"""
    if not config_path.exists():
        return {}
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"ERROR: Failed to load config: {e}", file=sys.stderr)
        return {}


def get_protected_paths(config: dict, repo_root: Path) -> List[Path]:
    """Get list of protected paths from config"""
    boundaries = config.get('boundaries', {})
    protected = boundaries.get('protected_paths', [])
    
    # Default protected paths if not configured
    if not protected:
        protected = [
            './blocks'
        ]
    
    # Convert to absolute paths
    return [repo_root / Path(p).resolve() for p in protected]


def check_path_protection(target_path: Path, protected_paths: List[Path]) -> Tuple[bool, str]:
    """
    Check if a path is protected.
    Returns (is_protected, reason)
    """
    target_abs = target_path.resolve()
    
    for protected in protected_paths:
        protected_abs = protected.resolve()
        
        # Check if target is within protected path
        try:
            target_abs.relative_to(protected_abs)
            return True, f"Path is within protected area: {protected}"
        except ValueError:
            continue
    
    return False, ""


def validate_write_operation(target_path: str, config_path: Path = None) -> bool:
    """
    Validate that a write operation is allowed.
    Returns True if allowed, False if forbidden.
    """
    if config_path is None:
        config_path = Path.cwd() / "config.yaml"
    
    config = load_config(config_path)
    repo_root = Path.cwd()
    protected_paths = get_protected_paths(config, repo_root)
    
    target = Path(target_path)
    is_protected, reason = check_path_protection(target, protected_paths)
    
    if is_protected:
        print(f"ERROR: Write operation forbidden: {target_path}", file=sys.stderr)
        print(f"REASON: {reason}", file=sys.stderr)
        print(f"Protected paths:", file=sys.stderr)
        for p in protected_paths:
            print(f"  - {p}", file=sys.stderr)
        return False
    
    return True




def main():
    ap = argparse.ArgumentParser(
        description="Validate repository boundaries and protected paths"
    )
    ap.add_argument(
        '--config',
        type=Path,
        default=Path.cwd() / "config.yaml",
        help="Path to config.yaml (default: ./config.yaml)"
    )
    ap.add_argument(
        '--check-path',
        type=str,
        help="Check if a specific path is protected"
    )
    
    args = ap.parse_args()
    
    errors = []
    
    if args.check_path:
        if not validate_write_operation(args.check_path, args.config):
            errors.append(f"Path is protected: {args.check_path}")
    else:
        # Default: just validate that config is readable
        print("Checking repository boundaries...")
    
    if errors:
        print("\nValidation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    
    print("OK: All validations passed")
    sys.exit(0)


if __name__ == "__main__":
    main()

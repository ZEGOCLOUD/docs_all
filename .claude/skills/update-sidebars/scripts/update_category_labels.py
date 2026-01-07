#!/usr/bin/env python3
"""
Update sidebar category labels using AI-provided translations.

This script reads a sidebars.json file and updates category labels
based on AI-generated translations. Categories are virtual groupings
without corresponding MDX files.

Usage:
1. Collect category labels using update_sidebar_labels.py
2. Use AI to translate the collected labels (only /en/ paths need translation)
3. Create a Python dict with the translations
4. Pass the translations to this script via --translations argument

IMPORTANT: This script must be run from the workspace root directory.
"""

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


def get_workspace_root() -> Path:
    """
    Find the workspace root directory by looking for marker files.

    Marker files (in order of priority):
    - docuo.config.json or docuo.config.en.json (DOCUO project)
    - .git (Git repository)
    - package.json (Node.js project)

    Returns:
        Path: workspace root directory

    Note:
        Falls back to current directory if no markers found.
    """
    current = Path.cwd().resolve()

    # Search up to 10 levels up
    for _ in range(10):
        markers = [
            'docuo.config.json',
            'docuo.config.en.json',
            '.git',
            'package.json'
        ]

        for marker in markers:
            if (current / marker).exists():
                return current

        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent

    # Fallback to current directory if no markers found
    return Path.cwd()


def process_category_item(
    item: Dict[str, Any],
    translations: Dict[str, str],
    dry_run: bool = False
) -> tuple[Dict[str, Any], bool]:
    """
    Process a single sidebar item, updating labels for category items.

    Args:
        item: Sidebar item dictionary
        translations: Dictionary mapping current labels to translated labels
        dry_run: If True, don't actually modify the item

    Returns:
        Tuple of (updated item dictionary, whether it was modified)
    """
    modified = False
    item_type = item.get('type')

    if item_type == 'category' and 'label' in item:
        current_label = item['label']

        # Check if label needs translation (exists in translations)
        if current_label in translations:
            new_label = translations[current_label]

            if new_label != current_label:
                print(f"{'[DRY RUN] ' if dry_run else ''}Update category: {current_label}")
                print(f"  New label: {new_label}")
                print()

                if not dry_run:
                    item['label'] = new_label
                modified = True

    # Recursively process nested items
    if 'items' in item:
        for i, sub_item in enumerate(item['items']):
            item['items'][i], sub_modified = process_category_item(sub_item, translations, dry_run)
            if sub_modified:
                modified = True

    return item, modified


def update_category_labels(
    sidebars_path: Path,
    translations: Dict[str, str],
    dry_run: bool = False
) -> bool:
    """
    Update all category labels in a sidebars.json file.

    Args:
        sidebars_path: Path to sidebars.json file
        translations: Dictionary mapping current labels to translated labels
        dry_run: If True, don't actually modify the file

    Returns:
        True if successful, False otherwise
    """
    # Read sidebars.json
    try:
        with open(sidebars_path, 'r', encoding='utf-8') as f:
            sidebars = json.load(f)
    except Exception as e:
        print(f"Error reading {sidebars_path}: {e}", file=sys.stderr)
        return False

    workspace_root = get_workspace_root()
    try:
        rel_path = sidebars_path.relative_to(workspace_root)
    except ValueError:
        rel_path = sidebars_path

    print(f"Processing: {rel_path}")
    if not translations:
        print("Warning: No translation mappings provided. No changes will be made.\n")
    print()

    # Process each sidebar
    modified = False
    for sidebar_name, items in sidebars.items():
        if isinstance(items, list):
            for i, item in enumerate(items):
                updated_item, item_modified = process_category_item(item, translations, dry_run)
                if item_modified:
                    modified = True
                sidebars[sidebar_name][i] = updated_item

    # Write back if modified
    if modified and not dry_run:
        try:
            with open(sidebars_path, 'w', encoding='utf-8') as f:
                json.dump(sidebars, f, ensure_ascii=False, indent=2)
            print(f"✅ Updated: {sidebars_path}")
        except Exception as e:
            print(f"Error writing {sidebars_path}: {e}", file=sys.stderr)
            return False
    elif dry_run and modified:
        print(f"[DRY RUN] Would update: {sidebars_path}")
    elif not modified:
        print(f"No changes needed")

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Update sidebar category labels with AI-generated translations',
        epilog="""
Example usage:
  # After collecting labels with update_sidebar_labels.py, use AI to translate them
  python3 scripts/update_category_labels.py path/to/sidebars.json \\
    --translations '{"产品简介": "Introduction", "快速开始": "Quick Start"}'

  # Batch update all sidebars
  python3 scripts/update_category_labels.py --all path/to/docs \\
    --translations '{"产品简介": "Introduction", "快速开始": "Quick Start"}'

Note: Only /en/ paths need translation. /zh/ paths should be skipped.
        """
    )
    parser.add_argument(
        'path',
        type=Path,
        help='Path to sidebars.json file or directory containing sidebars.json files'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Update all sidebars.json files in the directory tree'
    )
    parser.add_argument(
        '--translations',
        type=str,
        required=True,
        help='Python dict string with translations (e.g., \'{"产品简介": "Introduction"}\')'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would change without actually modifying files'
    )

    args = parser.parse_args()

    # Parse translations from string
    try:
        translations = ast.literal_eval(args.translations)
        if not isinstance(translations, dict):
            raise ValueError("Translations must be a dictionary")
    except Exception as e:
        print(f"Error parsing translations: {e}", file=sys.stderr)
        print("Translations must be a valid Python dict string, e.g., '{\"产品简介\": \"Introduction\"}'", file=sys.stderr)
        return 1

    if args.all:
        # Find all sidebars.json files
        if args.path.is_dir():
            sidebars_files = sorted(args.path.rglob('sidebars.json'))
        else:
            sidebars_files = [args.path]

        if not sidebars_files:
            print("No sidebars.json files found")
            return 1

        print(f"Found {len(sidebars_files)} sidebars.json files\\n")

        for sidebars_path in sidebars_files:
            update_category_labels(sidebars_path, translations, dry_run=args.dry_run)
            print("-" * 80)
            print()
    else:
        # Process single file or directory
        path = args.path

        if path.is_file() and path.name == 'sidebars.json':
            sidebars_path = path
        elif path.is_dir():
            # Look for sidebars.json in the directory
            sidebars_path = path / 'sidebars.json'
            if not sidebars_path.exists():
                print(f"Error: No sidebars.json found in {path}", file=sys.stderr)
                return 1
        else:
            print(f"Error: Invalid path {path}", file=sys.stderr)
            return 1

        if not update_category_labels(sidebars_path, translations, dry_run=args.dry_run):
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())

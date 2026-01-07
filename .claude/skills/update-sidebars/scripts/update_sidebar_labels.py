#!/usr/bin/env python3
"""
Update sidebar labels by extracting H1 headings from MDX files.

This script reads a sidebars.json file, finds all doc items with IDs,
locates the corresponding MDX files, extracts the first H1 heading,
and updates the label field.

Document ID resolution follows DOCUO rules:
- Relative to instance directory
- No file extension (.mdx)
- Uses / as path separator
- Lowercase with hyphens
- Number prefixes (01-, 02-) are removed

IMPORTANT: This script must be run from the workspace root directory.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


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


def normalize_document_id(doc_id: str) -> str:
    """
    Normalize document ID according to DOCUO conversion rules.

    Rules:
    1. Convert to lowercase
    2. Replace spaces with hyphens
    3. URL-encoded spaces (%20) become hyphens
    4. Windows backslashes become forward slashes
    5. Number prefixes (01-, 02-) are removed

    Args:
        doc_id: The document ID from sidebars.json

    Returns:
        Normalized document ID
    """
    # Already normalized IDs are returned as-is
    # This function is primarily for handling any edge cases
    doc_id = doc_id.lower()
    doc_id = doc_id.replace(' ', '-')
    doc_id = doc_id.replace('%20', '-')
    doc_id = doc_id.replace('\\', '/')
    return doc_id


def find_mdx_file(instance_dir: Path, doc_id: str) -> Optional[Path]:
    """
    Find the MDX file corresponding to a document ID.

    Tries multiple file extensions and handles number prefixes.

    Args:
        instance_dir: Path to the instance directory
        doc_id: Document ID (may include number prefixes)

    Returns:
        Path to the MDX file if found, None otherwise
    """
    # Common extensions to try
    extensions = ['.mdx', '.md']

    # Try direct path first
    for ext in extensions:
        direct_path = instance_dir / f"{doc_id}{ext}"
        if direct_path.exists():
            return direct_path

    # Try with number prefixes (01-, 02-, etc.)
    parts = doc_id.split('/')
    for i, part in enumerate(parts):
        # Try with number prefix
        for num in range(1, 100):
            prefixed = f"{num:02d}-{part}"
            prefixed_parts = parts.copy()
            prefixed_parts[i] = prefixed
            prefixed_id = '/'.join(prefixed_parts)

            for ext in extensions:
                prefixed_path = instance_dir / f"{prefixed_id}{ext}"
                if prefixed_path.exists():
                    return prefixed_path

    return None


def is_suitable_label(h1_text: str) -> bool:
    """
    Check if H1 text is suitable for sidebar label.

    Args:
        h1_text: The H1 text to check

    Returns:
        True if suitable for sidebar label, False otherwise
    """
    # Skip if contains HTML tags (common for images, complex formatting)
    if '<' in h1_text and '>' in h1_text:
        return False

    # Skip if too long (> 100 chars is probably too long for sidebar)
    if len(h1_text) > 100:
        return False

    # Skip if only special characters/numbers
    if not any(c.isalpha() for c in h1_text):
        return False

    return True


def extract_import_source(content: str, mdx_file: Path, workspace_root: Path = None) -> Optional[Path]:
    """
    Extract the source file path from import statements.

    Args:
        content: File content
        mdx_file: Path to the current MDX file (for resolving relative paths)
        workspace_root: Path to the workspace root (for resolving absolute paths)

    Returns:
        Path to the imported source file, or None if not found
    """
    import re

    # Match patterns like:
    # import Content from '/path/to/file.mdx'
    # import Content from "../path/to/file.mdx"
    # import { Content } from './path/to/file.mdx'

    patterns = [
        r"import\s+Content\s+from\s+['\"]([^'\"]+)['\"]",
        r"import\s+\{\s*Content\s*\}\s+from\s+['\"]([^'\"]+)['\"]",
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            import_path = match.group(1)

            # Handle absolute paths (starting with /)
            if import_path.startswith('/'):
                # Remove leading slash and make relative to workspace root
                import_path = import_path.lstrip('/')
                if workspace_root:
                    return workspace_root / import_path
                else:
                    # Fallback: try to find workspace root by going up from mdx_file
                    # Look for common markers like docuo.config.json, package.json, etc.
                    current = mdx_file.resolve()
                    for _ in range(10):  # Go up at most 10 levels
                        if (current / 'docuo.config.json').exists() or \
                           (current / 'docuo.config.en.json').exists() or \
                           (current / 'package.json').exists():
                            return current / import_path
                        parent = current.parent
                        if parent == current:  # Reached root
                            break
                        current = parent
                    # Last resort: use Path.cwd()
                    return Path.cwd() / import_path

            # Handle relative paths
            else:
                # Resolve relative to the current file's directory
                current_dir = mdx_file.parent
                resolved_path = (current_dir / import_path).resolve()

                # Check if resolved path exists
                if resolved_path.exists():
                    return resolved_path

    return None


def extract_first_h1(mdx_file: Path, follow_imports: bool = True, visited: set = None, workspace_root: Path = None) -> Optional[str]:
    """
    Extract the first H1 heading from an MDX file.

    Args:
        mdx_file: Path to the MDX file
        follow_imports: Whether to follow import statements to source files
        visited: Set of already visited files (to prevent circular imports)
        workspace_root: Path to the workspace root (for resolving absolute import paths)

    Returns:
        The H1 text without the # prefix, or None if not found or not suitable
    """
    if visited is None:
        visited = set()

    # Prevent circular imports
    mdx_key = str(mdx_file.resolve())
    if mdx_key in visited:
        return None
    visited.add(mdx_key)

    try:
        with open(mdx_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip frontmatter (between --- markers)
        lines = content.split('\n')
        start_idx = 0
        if lines[0].strip() == '---':
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    start_idx = i + 1
                    break

        # Find first H1 heading in current file
        for line in lines[start_idx:]:
            line = line.strip()
            if line.startswith('# '):
                # Extract H1 text
                h1_text = line[2:].strip()

                # Check if suitable for sidebar label
                if is_suitable_label(h1_text):
                    return h1_text
                else:
                    # H1 exists but not suitable (e.g., contains HTML)
                    return None

        # No suitable H1 found in current file, check if this file imports content from another file
        if follow_imports:
            import_source = extract_import_source(content, mdx_file, workspace_root)
            if import_source:
                # Recursively extract H1 from the imported source file
                return extract_first_h1(import_source, follow_imports=True, visited=visited, workspace_root=workspace_root)

        return None
    except Exception as e:
        print(f"Error reading {mdx_file}: {e}", file=sys.stderr)
        return None


def process_sidebar_item(
    item: Dict[str, Any],
    instance_dir: Path,
    dry_run: bool = False,
    external_links: Dict[str, List[Dict]] = None,
    tag_labels: Dict[str, List[Dict]] = None,
    category_labels: Dict[str, List[Dict]] = None,
    current_path: List[str] = None,
    workspace_root: Path = None
) -> tuple[Dict[str, Any], bool, Dict[str, List[Dict]], Dict[str, List[Dict]], Dict[str, List[Dict]]]:
    """
    Process a single sidebar item, updating labels for doc and link items.

    Args:
        item: Sidebar item dictionary
        instance_dir: Path to the instance directory
        dry_run: If True, don't actually modify the item
        external_links: Dictionary to collect external links that need translation
        tag_labels: Dictionary to collect tag labels that need translation
        category_labels: Dictionary to collect category labels that need translation
        current_path: Current path in the sidebar structure (for tracking)
        workspace_root: Path to the workspace root (for resolving absolute import paths)

    Returns:
        Tuple of (updated item, modified, external_links, tag_labels, category_labels)
    """
    if external_links is None:
        external_links = {'en': [], 'zh': [], 'unknown': []}
    if tag_labels is None:
        tag_labels = {'en': [], 'zh': [], 'unknown': []}
    if category_labels is None:
        category_labels = {'en': [], 'zh': [], 'unknown': []}
    if current_path is None:
        current_path = []

    modified = False
    item_type = item.get('type')

    if item_type == 'doc' and 'id' in item:
        doc_id = item['id']
        current_label = item.get('label', '')

        # Find the MDX file
        mdx_file = find_mdx_file(instance_dir, doc_id)

        if mdx_file:
            # Extract H1
            h1_text = extract_first_h1(mdx_file, workspace_root=workspace_root)

            if h1_text:
                if h1_text != current_label:
                    print(f"{'[DRY RUN] ' if dry_run else ''}Update: {doc_id}")
                    print(f"  Old label: {current_label}")
                    print(f"  New label: {h1_text}")
                    print(f"  Source: {mdx_file.relative_to(instance_dir.parent.parent)}")
                    print()

                    if not dry_run:
                        item['label'] = h1_text
                    modified = True
            else:
                # H1 not found or not suitable (e.g., contains HTML, or import failed)
                # Read file to determine reason
                try:
                    with open(mdx_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check if this is an import file
                    import_source = extract_import_source(content, mdx_file, workspace_root=workspace_root)
                    if import_source:
                        try:
                            print(f"Skip (import source has no suitable H1): {doc_id} -> {import_source.relative_to(get_workspace_root())}")
                        except ValueError:
                            print(f"Skip (import source has no suitable H1): {doc_id} -> {import_source}")
                    else:
                        # Check if file has any H1 after frontmatter
                        # Handle multiple --- separators (some files have frontmatter with ---)
                        lines = content.split('\n')
                        start_idx = 0
                        if lines[0].strip() == '---':
                            for i, line in enumerate(lines[1:], 1):
                                if line.strip() == '---':
                                    start_idx = i + 1
                                    break

                        rest_content = '\n'.join(lines[start_idx:])
                        has_h1 = '# ' in rest_content

                        if has_h1:
                            print(f"Skip (H1 not suitable - contains HTML/oversized): {doc_id}")
                        else:
                            print(f"Skip (no H1): {doc_id} - {mdx_file.name}")
                except:
                    print(f"Skip (no H1): {doc_id} - {mdx_file.name}")
        else:
            print(f"Skip (file not found): {doc_id}")

        # Check for tag.label in doc items - collect all tags regardless of language
        if 'tag' in item and isinstance(item['tag'], dict) and 'label' in item['tag']:
            tag_label_current = item['tag']['label']

            # Detect language from instance directory
            locale = 'unknown'
            instance_path_str = str(instance_dir)
            if '/en/' in instance_path_str or instance_path_str.endswith('/en'):
                locale = 'en'
            elif '/zh/' in instance_path_str or instance_path_str.endswith('/zh'):
                locale = 'zh'

            # Collect all tags (will be filtered by locale in report)
            tag_labels[locale].append({
                'file': str(instance_dir / 'sidebars.json'),
                'context_id': doc_id,
                'label': tag_label_current,
                'path': ' -> '.join(current_path)
            })

            print(f"Collect (tag label): {tag_label_current} (in {doc_id}, locale={locale})")

    elif item_type == 'link' and 'href' in item:
        href = item['href']
        current_label = item.get('label', '')

        # Detect if label needs translation (has Chinese characters)
        has_chinese = any('\u4e00' <= ch <= '\u9fff' for ch in current_label)

        if not has_chinese:
            # Label already translated, skip
            pass
        elif href.startswith('http://') or href.startswith('https://'):
            # External link - collect for manual translation
            # Detect language from instance directory
            locale = 'unknown'
            instance_path_str = str(instance_dir)
            if '/en/' in instance_path_str or instance_path_str.endswith('/en'):
                locale = 'en'
            elif '/zh/' in instance_path_str or instance_path_str.endswith('/zh'):
                locale = 'zh'

            external_links[locale].append({
                'file': str(instance_dir / 'sidebars.json'),
                'href': href,
                'label': current_label,
                'path': ' -> '.join(current_path)
            })

            print(f"Collect (external link): {current_label} -> {href}")

        elif href.startswith('/'):
            # Internal link - resolve to MDX file and extract H1
            # Detect locale from instance directory
            locale = 'zh'  # default
            instance_path_str = str(instance_dir)
            if '/en/' in instance_path_str or instance_path_str.endswith('/en'):
                locale = 'en'

            mdx_file = resolve_internal_link(href, locale)

            if mdx_file and mdx_file.exists():
                h1_text = extract_first_h1(mdx_file, workspace_root=workspace_root)

                if h1_text and h1_text != current_label:
                    print(f"{'[DRY RUN] ' if dry_run else ''}Update link: {current_label}")
                    print(f"  Old label: {current_label}")
                    print(f"  New label: {h1_text}")
                    try:
                        print(f"  Source: {href} -> {mdx_file.relative_to(get_workspace_root())}")
                    except ValueError:
                        print(f"  Source: {href} -> {mdx_file}")
                    print(f"  Config: docuo.config.{locale}.json")
                    print()

                    if not dry_run:
                        item['label'] = h1_text
                    modified = True
                else:
                    print(f"Skip (link target has no suitable H1): {current_label} -> {href}")
            else:
                print(f"Skip (cannot resolve link): {current_label} -> {href}")

        # Check for tag.label in link items - collect all tags regardless of language
        if 'tag' in item and isinstance(item['tag'], dict) and 'label' in item['tag']:
            tag_label_current = item['tag']['label']

            # Detect language from instance directory
            locale = 'unknown'
            instance_path_str = str(instance_dir)
            if '/en/' in instance_path_str or instance_path_str.endswith('/en'):
                locale = 'en'
            elif '/zh/' in instance_path_str or instance_path_str.endswith('/zh'):
                locale = 'zh'

            # Collect all tags (will be filtered by locale in report)
            tag_labels[locale].append({
                'file': str(instance_dir / 'sidebars.json'),
                'context_id': href,
                'label': tag_label_current,
                'path': ' -> '.join(current_path)
            })

            print(f"Collect (tag label): {tag_label_current} (in {href}, locale={locale})")

    elif item_type == 'category' and 'items' in item:
        # Collect all category labels regardless of language
        category_label = item.get('label', '')
        if category_label:
            # Detect language from instance directory
            locale = 'unknown'
            instance_path_str = str(instance_dir)
            if '/en/' in instance_path_str or instance_path_str.endswith('/en'):
                locale = 'en'
            elif '/zh/' in instance_path_str or instance_path_str.endswith('/zh'):
                locale = 'zh'

            # Collect all categories (will be filtered by locale in report)
            category_labels[locale].append({
                'file': str(instance_dir / 'sidebars.json'),
                'label': category_label,
                'path': ' -> '.join(current_path)
            })

            print(f"Collect (category label): {category_label} (locale={locale})")

        # Recursively process category items
        new_path = current_path + [f"category:{category_label}"]

        for i, sub_item in enumerate(item['items']):
            item['items'][i], sub_modified, sub_links, sub_tags, sub_cats = process_sidebar_item(
                sub_item, instance_dir, dry_run, external_links, tag_labels, category_labels, new_path, workspace_root
            )
            if sub_modified:
                modified = True
            # Note: external_links, tag_labels, and category_labels are modified in place by recursive calls
            # No need to extend/merge them again (sub_cats, sub_links, sub_tags are the same objects)
            _ = sub_cats  # Explicitly mark as intentionally unused

    return item, modified, external_links, tag_labels, category_labels


def update_sidebar_labels(
    sidebars_path: Path,
    instance_dir: Optional[Path] = None,
    dry_run: bool = False
) -> bool:
    """
    Update all labels in a sidebars.json file.

    Args:
        sidebars_path: Path to sidebars.json file
        instance_dir: Path to instance directory (defaults to sidebars parent)
        dry_run: If True, don't actually modify the file

    Returns:
        True if successful, False otherwise
    """
    # Determine instance directory
    if instance_dir is None:
        instance_dir = sidebars_path.parent

    # Determine workspace root by looking for docuo config files
    workspace_root = None
    current = sidebars_path.resolve()
    for _ in range(10):  # Go up at most 10 levels
        if (current / 'docuo.config.json').exists() or \
           (current / 'docuo.config.en.json').exists() or \
           (current / 'package.json').exists():
            workspace_root = current
            break
        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent

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
    try:
        rel_instance = instance_dir.relative_to(workspace_root)
    except ValueError:
        rel_instance = instance_dir

    print(f"Processing: {rel_path}")
    print(f"Instance directory: {rel_instance}")
    print()

    # Process each sidebar
    modified = False
    all_external_links = {'en': [], 'zh': [], 'unknown': []}
    all_tag_labels = {'en': [], 'zh': [], 'unknown': []}
    all_category_labels = {'en': [], 'zh': [], 'unknown': []}

    for sidebar_name, items in sidebars.items():
        if isinstance(items, list):
            for i, item in enumerate(items):
                updated_item, item_modified, external_links, tag_labels, category_labels = process_sidebar_item(
                    item, instance_dir, dry_run, workspace_root=workspace_root
                )
                if item_modified:
                    modified = True
                sidebars[sidebar_name][i] = updated_item

                # Collect external links, tag labels, and category labels
                for locale in all_external_links:
                    all_external_links[locale].extend(external_links[locale])
                    all_tag_labels[locale].extend(tag_labels[locale])
                    all_category_labels[locale].extend(category_labels[locale])

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

    # Output external links report - only show /en/ locale (needs translation)
    if all_external_links['en']:
        print("\n" + "=" * 80)
        print("External links requiring AI translation (/en/ only):")
        print("=" * 80)

        print(f"\nEN ({len(all_external_links['en'])} links):")
        for link in all_external_links['en']:
            print(f"  File: {link['file']}")
            print(f"  Path: {link['path']}")
            print(f"  Label: {link['label']}")
            print(f"  Href: {link['href']}")
            print()

        print("=" * 80)
        print("💡 Tip: /zh/ paths don't need translation. Use AI to translate /en/ labels, then apply with update_external_link_labels.py")
        print("=" * 80)

    # Output tag labels report - only show /en/ locale (needs translation)
    if all_tag_labels['en']:
        print("\n" + "=" * 80)
        print("Tag labels requiring AI translation (/en/ only):")
        print("=" * 80)

        print(f"\nEN ({len(all_tag_labels['en'])} tags):")
        for tag in all_tag_labels['en']:
            print(f"  File: {tag['file']}")
            print(f"  Path: {tag['path']}")
            print(f"  Context: {tag['context_id']}")
            print(f"  Label: {tag['label']}")
            print()

        print("=" * 80)
        print("💡 Tip: /zh/ paths don't need translation. Use AI to translate /en/ labels, then apply with update_tag_labels.py")
        print("=" * 80)

    # Output category labels report - only show /en/ locale (needs translation)
    if all_category_labels['en']:
        print("\n" + "=" * 80)
        print("Category labels requiring AI translation (/en/ only):")
        print("=" * 80)

        print(f"\nEN ({len(all_category_labels['en'])} categories):")
        for cat in all_category_labels['en']:
            print(f"  File: {cat['file']}")
            print(f"  Path: {cat['path']}")
            print(f"  Label: {cat['label']}")
            print()

        print("=" * 80)
        print("💡 Tip: /zh/ paths don't need translation. Use AI to translate /en/ labels, then apply with update_category_labels.py")
        print("=" * 80)

    return True


def find_docuo_config(locale: str = 'zh') -> Optional[Path]:
    """
    Find the docuo configuration file for a specific locale.

    Tries to find docuo.config.{locale}.json first, falling back to docuo.config.json

    Args:
        locale: Language locale ('zh' or 'en')

    Returns:
        Path to the config file, or None if not found
    """
    workspace_root = get_workspace_root()

    # Try locale-specific config first
    locale_config = workspace_root / f'docuo.config.{locale}.json'
    if locale_config.exists():
        return locale_config

    # Fall back to main config
    main_config = workspace_root / 'docuo.config.json'
    if main_config.exists():
        return main_config

    return None


def load_instance_config(route_base_path: str, locale: str = 'zh') -> Optional[Dict[str, Any]]:
    """
    Load instance configuration from docuo.config.{locale}.json matching a routeBasePath.

    Args:
        route_base_path: The routeBasePath to match (e.g., 'real-time-video-android-java')
        locale: Language locale ('zh' or 'en', defaults to 'zh')

    Returns:
        Instance configuration dict, or None if not found
    """
    config_path = find_docuo_config(locale)
    if not config_path:
        return None

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        instances = config.get('instances', [])
        for instance in instances:
            if instance.get('routeBasePath') == route_base_path:
                return instance

        return None
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        return None


def resolve_internal_link(href: str, locale: str = 'zh') -> Optional[Path]:
    """
    Resolve an internal link (/path) to an MDX file.

    Args:
        href: Internal link path (e.g., '/real-time-video-android-ja/faq/connect-to-zego-mcp-server')
        locale: Language locale ('zh' or 'en', defaults to 'zh')

    Returns:
        Path to the MDX file, or None if not found
    """
    # Remove leading slash and split into parts
    href = href.lstrip('/')
    parts = href.split('/', 1)

    if len(parts) < 2:
        return None

    route_base_path = parts[0]
    doc_path = parts[1] if len(parts) > 1 else None

    if not doc_path:
        return None

    # Load instance config with the correct locale
    instance = load_instance_config(route_base_path, locale)
    if not instance:
        return None

    # Get instance directory
    instance_dir = get_workspace_root() / instance['path']

    # Convert path to document ID
    # Remove .mdx or .html extension if present
    doc_id = re.sub(r'\.(mdx|html)$', '', doc_path)

    # Find the MDX file
    return find_mdx_file(instance_dir, doc_id)


def find_all_sidebars(root_dir: Path) -> List[Path]:
    """
    Find all sidebars.json files in the project.

    Args:
        root_dir: Root directory to search

    Returns:
        List of paths to sidebars.json files
    """
    sidebars_files = list(root_dir.rglob('sidebars.json'))
    return sorted(sidebars_files)


def main():
    parser = argparse.ArgumentParser(
        description='Update sidebar labels from MDX H1 headings'
    )
    parser.add_argument(
        'path',
        nargs='?',
        type=Path,
        default=Path.cwd(),
        help='Path to sidebars.json file or instance directory (default: current directory)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Update all sidebars.json files in the project'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would change without actually modifying files'
    )
    parser.add_argument(
        '--root',
        type=Path,
        default=Path.cwd(),
        help='Root directory for --all search (default: current directory)'
    )

    args = parser.parse_args()

    if args.all:
        # Find all sidebars.json files
        sidebars_files = find_all_sidebars(args.root)
        if not sidebars_files:
            print("No sidebars.json files found")
            return 1

        print(f"Found {len(sidebars_files)} sidebars.json files\n")

        for sidebars_path in sidebars_files:
            update_sidebar_labels(sidebars_path, dry_run=args.dry_run)
            print("-" * 80)
            print()
    else:
        # Process specific file or directory
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

        if not update_sidebar_labels(sidebars_path, dry_run=args.dry_run):
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
Metadata Validation Script for W3 Governance Automation
========================================================

This script validates metadata fields in markdown files according to W3 governance rules.
Key validation: If 'approved-by' is present, 'reason' must also be present.

Team members (valid paths):
- BBX19
- Copilot-Gm
- ChatGPT
- Gemini
- Grok
- DeepSeek
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# Valid team member directories
TEAM_MEMBER_PATHS = [
    "BBX19",
    "Copilot-Gm",
    "ChatGPT",
    "Gemini",
    "Grok",
    "DeepSeek",
]


def extract_metadata(content: str) -> Dict[str, str]:
    """
    Extract metadata fields from markdown content.
    Looks for patterns like 'field-name: value' at the beginning of lines.
    """
    metadata = {}
    # Match patterns like 'approved-by: BBX19' or 'reason: system-alignment-ok'
    pattern = r'^([a-zA-Z][a-zA-Z0-9_-]*)\s*:\s*(.+)$'
    
    for line in content.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            key = match.group(1).lower()
            value = match.group(2).strip()
            metadata[key] = value
    
    return metadata


def validate_approval_reason(metadata: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    """
    Validate that if 'approved-by' is present, 'reason' must also be present.
    Returns (is_valid, error_message).
    """
    has_approval = 'approved-by' in metadata
    has_reason = 'reason' in metadata
    
    if has_approval and not has_reason:
        return False, "Error: 'approved-by' field found but 'reason' field is missing. Every approval must have a reason."
    
    return True, None


def validate_file(file_path: str) -> List[str]:
    """
    Validate a single file for metadata compliance.
    Returns a list of error messages.
    """
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Error reading file {file_path}: {e}")
        return errors
    
    metadata = extract_metadata(content)
    
    # Validate approval-reason pairing
    is_valid, error = validate_approval_reason(metadata)
    if not is_valid:
        errors.append(f"{file_path}: {error}")
    
    return errors


def find_markdown_files(root_dir: str) -> List[str]:
    """
    Find all markdown files in the specified directories.
    """
    markdown_files = []
    
    for team_path in TEAM_MEMBER_PATHS:
        team_dir = Path(root_dir) / team_path
        if team_dir.exists():
            for md_file in team_dir.rglob('*.md'):
                markdown_files.append(str(md_file))
    
    return markdown_files


def main():
    """Main entry point for the validation script."""
    # Get the repository root directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    print("=" * 60)
    print("W3 Governance Metadata Validation")
    print("=" * 60)
    print()
    print(f"Scanning team member directories: {', '.join(TEAM_MEMBER_PATHS)}")
    print()
    
    # Find all markdown files
    markdown_files = find_markdown_files(repo_root)
    
    if not markdown_files:
        print("No markdown files found in team member directories.")
        return 0
    
    print(f"Found {len(markdown_files)} markdown file(s) to validate.")
    print()
    
    # Validate all files
    all_errors = []
    for file_path in markdown_files:
        errors = validate_file(file_path)
        all_errors.extend(errors)
    
    # Report results
    if all_errors:
        print("VALIDATION FAILED")
        print("-" * 40)
        for error in all_errors:
            print(f"  ❌ {error}")
        print()
        print(f"Total errors: {len(all_errors)}")
        return 1
    else:
        print("✅ VALIDATION PASSED")
        print("-" * 40)
        print("All files comply with governance metadata rules.")
        print()
        print("Validated rules:")
        print("  • If 'approved-by' is present, 'reason' must also be present")
        return 0


if __name__ == "__main__":
    sys.exit(main())

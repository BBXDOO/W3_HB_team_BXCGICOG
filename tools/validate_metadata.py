#!/usr/bin/env python3
"""
Metadata Validator for W3 Governance-as-Code

This script validates markdown files across specified directories.
It checks for file existence, readability, and minimum content requirements.

Usage:
    python validate_metadata.py --paths "BBX19/**/*.md" "Copilot-Gm/**/*.md" ...
"""

import argparse
import glob
import os
import sys

# Minimum content length for a valid markdown file
MIN_CONTENT_LENGTH = 10


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate metadata in markdown files"
    )
    parser.add_argument(
        "--paths",
        nargs="+",
        required=True,
        help="Glob patterns for markdown files to validate"
    )
    return parser.parse_args()


def find_files(patterns):
    """Find all files matching the given glob patterns."""
    files = []
    for pattern in patterns:
        matched = glob.glob(pattern, recursive=True)
        files.extend(matched)
    return sorted(set(files))


def validate_markdown_file(filepath):
    """
    Validate a single markdown file.
    
    Returns:
        tuple: (is_valid, list of issues)
    """
    issues = []
    
    # Check if file exists and is readable
    if not os.path.exists(filepath):
        return False, [f"File does not exist: {filepath}"]
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                content = f.read()
        except Exception as e:
            return False, [f"Cannot read file: {e}"]
    except Exception as e:
        return False, [f"Cannot read file: {e}"]
    
    # Check for empty file
    if not content.strip():
        issues.append("File is empty")
    
    # Check for minimum content length
    if len(content.strip()) < MIN_CONTENT_LENGTH:
        issues.append(f"File content is too short (less than {MIN_CONTENT_LENGTH} characters)")
    
    return len(issues) == 0, issues


def main():
    """Main entry point."""
    args = parse_args()
    
    print("=" * 60)
    print("W3 Governance Metadata Validator")
    print("=" * 60)
    print()
    
    # Find all matching files
    print(f"Searching for files with patterns: {args.paths}")
    files = find_files(args.paths)
    
    if not files:
        print("\n⚠️  No files found matching the specified patterns.")
        print("This may be expected if the directories are empty or patterns don't match any files.")
        print("Validation passed (no files to validate).")
        return 0
    
    print(f"\nFound {len(files)} file(s) to validate:\n")
    
    # Validate each file
    total_files = len(files)
    valid_files = 0
    invalid_files = 0
    all_issues = []
    
    for filepath in files:
        is_valid, issues = validate_markdown_file(filepath)
        
        if is_valid:
            print(f"  ✅ {filepath}")
            valid_files += 1
        else:
            print(f"  ❌ {filepath}")
            for issue in issues:
                print(f"      - {issue}")
            invalid_files += 1
            all_issues.append((filepath, issues))
    
    # Summary
    print()
    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)
    print(f"  Total files:   {total_files}")
    print(f"  Valid files:   {valid_files}")
    print(f"  Invalid files: {invalid_files}")
    print()
    
    if invalid_files > 0:
        print("❌ Validation FAILED")
        print("\nIssues found:")
        for filepath, issues in all_issues:
            print(f"\n  {filepath}:")
            for issue in issues:
                print(f"    - {issue}")
        return 1
    else:
        print("✅ Validation PASSED")
        return 0


if __name__ == "__main__":
    sys.exit(main())

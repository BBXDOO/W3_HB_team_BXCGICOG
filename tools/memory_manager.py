#!/usr/bin/env python3
"""
Memory Manager Script for W3 JSON Brain
========================================

This script manages the central memory bank (knowledge/memory_bank.json).
Provides CLI commands for adding and searching memories.

Usage:
    python memory_manager.py add --tags "tag1,tag2" --content "Your content here"
    python memory_manager.py search --keyword "search term"
    python memory_manager.py search --tags "tag1,tag2"
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def get_memory_bank_path() -> Path:
    """Get the path to the memory bank JSON file."""
    script_dir = Path(__file__).parent
    return script_dir.parent / "knowledge" / "memory_bank.json"


def load_memory_bank() -> dict:
    """Load the memory bank from JSON file."""
    path = get_memory_bank_path()
    if not path.exists():
        return {
            "meta": {"version": "1.0", "last_updated": ""},
            "memories": []
        }
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory_bank(data: dict) -> None:
    """Save the memory bank to JSON file."""
    path = get_memory_bank_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data["meta"]["last_updated"] = datetime.now().isoformat()
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_memory(tags: List[str], content: str) -> dict:
    """
    Add a new memory to the memory bank.
    
    Args:
        tags: List of tags for the memory
        content: The content of the memory
        
    Returns:
        The newly created memory entry
    """
    data = load_memory_bank()
    
    # Generate next ID based on max existing ID + 1 to avoid collisions
    next_id = 1
    if data["memories"]:
        next_id = max(m["id"] for m in data["memories"]) + 1
    
    memory = {
        "id": next_id,
        "timestamp": datetime.now().isoformat(),
        "tags": tags,
        "content": content
    }
    
    data["memories"].append(memory)
    save_memory_bank(data)
    
    return memory


def search_memories(keyword: Optional[str] = None, tags: Optional[List[str]] = None) -> List[dict]:
    """
    Search memories by keyword or tags.
    
    Args:
        keyword: Search term to look for in content
        tags: List of tags to filter by
        
    Returns:
        List of matching memories
    """
    data = load_memory_bank()
    results = []
    
    for memory in data["memories"]:
        match = True
        
        if keyword:
            if keyword.lower() not in memory["content"].lower():
                match = False
        
        if tags:
            memory_tags = [t.lower() for t in memory["tags"]]
            if not any(tag.lower() in memory_tags for tag in tags):
                match = False
        
        if match:
            results.append(memory)
    
    return results


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="W3 JSON Brain Memory Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Add a memory:
    python memory_manager.py add --tags "python,learning" --content "Learned about decorators"
  
  Search by keyword:
    python memory_manager.py search --keyword "decorators"
  
  Search by tags:
    python memory_manager.py search --tags "python,learning"
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new memory")
    add_parser.add_argument(
        "--tags", "-t",
        required=True,
        help="Comma-separated tags for the memory"
    )
    add_parser.add_argument(
        "--content", "-c",
        required=True,
        help="Content of the memory"
    )
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument(
        "--keyword", "-k",
        help="Keyword to search in content"
    )
    search_parser.add_argument(
        "--tags", "-t",
        help="Comma-separated tags to filter by"
    )
    
    args = parser.parse_args()
    
    if args.command == "add":
        tags = [tag.strip() for tag in args.tags.split(",")]
        memory = add_memory(tags, args.content)
        print(f"✅ Memory added successfully!")
        print(f"   ID: {memory['id']}")
        print(f"   Tags: {', '.join(memory['tags'])}")
        print(f"   Timestamp: {memory['timestamp']}")
        
    elif args.command == "search":
        if not args.keyword and not args.tags:
            print("❌ Please provide --keyword or --tags for search")
            sys.exit(1)
        
        tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else None
        results = search_memories(keyword=args.keyword, tags=tags)
        
        if results:
            print(f"🔍 Found {len(results)} memory(ies):")
            print("-" * 40)
            for memory in results:
                print(f"  ID: {memory['id']}")
                print(f"  Tags: {', '.join(memory['tags'])}")
                print(f"  Timestamp: {memory['timestamp']}")
                print(f"  Content: {memory['content']}")
                print("-" * 40)
        else:
            print("🔍 No memories found matching your criteria.")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

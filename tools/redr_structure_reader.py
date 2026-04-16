#!/usr/bin/env python3
"""
REDR (Reader) - Structure Reader & Classifier
Role: Structure Reader & Classifier
Priority: HIGH

Functions:
- Read entire repository structure
- Classify into categories
- Detect case sensitivity issues
- Identify ghost folders
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class REDRReader:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.structure = defaultdict(list)
        self.categories = {
            'core_system': [],
            'w3lgu': [],
            'docs_pwa': [],
            'experimental': [],
            'modules': [],
            'tools': [],
            'deprecated': []
        }
        self.case_issues = []
        self.ghost_folders = []
        self.empty_folders = []
        
    def categorize_path(self, path):
        """Categorize a path into one of the main categories"""
        path_str = str(path).lower()
        
        # Core System
        if any(x in path_str for x in ['core/', 'bbex-core/', 'system/', 'architecture/', 'blueprints/']):
            return 'core_system'
        
        # W3Lgu
        if 'w3lgu' in path_str:
            return 'w3lgu'
        
        # Documentation / PWA
        if any(x in path_str for x in ['docs/', 'readme', 'branding/', 'meta/']):
            return 'docs_pwa'
        
        # Experimental / Dust
        if any(x in path_str for x in ['test', 'prototype', 'experiment', 'lab', 'studio']):
            return 'experimental'
        
        # Module directories
        if any(x in path_str for x in ['chatgpt/', 'gemini/', 'grok/', 'deepseek/', 'copilot-gm/', 'bbx19/']):
            return 'modules'
        
        # Tools
        if 'tools/' in path_str or 'scripts/' in path_str:
            return 'tools'
        
        # Deprecated (old Copilot folder)
        if 'copilot/' in path_str and 'copilot-gm' not in path_str:
            return 'deprecated'
        
        return 'experimental'
    
    def check_case_sensitivity(self):
        """Check for potential case sensitivity issues"""
        seen_lowercase = {}
        
        for root, dirs, files in os.walk(self.repo_path):
            current_path = Path(root)
            
            # Skip .git directory
            if '.git' in current_path.parts:
                continue
            
            # Check directories
            for dir_name in dirs:
                lower_name = dir_name.lower()
                if lower_name in seen_lowercase:
                    self.case_issues.append({
                        'type': 'directory',
                        'path1': str(seen_lowercase[lower_name]),
                        'path2': str(current_path / dir_name),
                        'issue': 'Similar names differing only in case'
                    })
                else:
                    seen_lowercase[lower_name] = current_path / dir_name
            
            # Check files
            for file_name in files:
                lower_name = file_name.lower()
                if lower_name in seen_lowercase:
                    existing = seen_lowercase[lower_name]
                    if existing.is_file():
                        self.case_issues.append({
                            'type': 'file',
                            'path1': str(existing),
                            'path2': str(current_path / file_name),
                            'issue': 'Similar names differing only in case'
                        })
                else:
                    seen_lowercase[lower_name] = current_path / file_name
    
    def find_ghost_folders(self):
        """Find empty directories that might be 'ghost' folders"""
        for root, dirs, files in os.walk(self.repo_path):
            current_path = Path(root)
            
            # Skip .git directory
            if '.git' in current_path.parts:
                continue
            
            # Check if directory is empty (no files, only subdirs might exist)
            if not files and not dirs:
                # Check if it's truly empty or has only .gitkeep
                gitkeep_path = current_path / '.gitkeep'
                if not gitkeep_path.exists():
                    self.empty_folders.append({
                        'path': str(current_path.relative_to(self.repo_path)),
                        'reason': 'Completely empty'
                    })
                else:
                    self.empty_folders.append({
                        'path': str(current_path.relative_to(self.repo_path)),
                        'reason': 'Has .gitkeep placeholder'
                    })
    
    def scan_structure(self):
        """Scan the entire repository structure"""
        print("📦 REDR Structure Reader Starting...")
        print(f"📂 Repository: {self.repo_path}")
        print()
        
        # Walk through directory structure
        print("🔍 Scanning directory structure...")
        for root, dirs, files in os.walk(self.repo_path):
            current_path = Path(root)
            
            # Skip .git directory
            if '.git' in current_path.parts:
                continue
            
            relative_path = current_path.relative_to(self.repo_path)
            
            # Categorize this path
            category = self.categorize_path(relative_path)
            
            # Add to structure
            item = {
                'path': str(relative_path),
                'type': 'directory',
                'file_count': len(files),
                'subdir_count': len(dirs),
                'category': category
            }
            
            self.structure[category].append(item)
            self.categories[category].append(str(relative_path))
        
        print(f"   Scanned structure")
        
        # Check for case sensitivity issues
        print("🔤 Checking case sensitivity...")
        self.check_case_sensitivity()
        print(f"   Found {len(self.case_issues)} potential issue(s)")
        
        # Find ghost folders
        print("👻 Finding ghost folders...")
        self.find_ghost_folders()
        print(f"   Found {len(self.empty_folders)} empty folder(s)")
        
        print()
        print("✅ Structure scan complete")
    
    def generate_report(self, output_path):
        """Generate structure map report"""
        report = []
        report.append("# REDR Structure Map Report")
        report.append("")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        report.append("---")
        report.append("")
        
        # Overview
        report.append("## 📊 Overview")
        report.append("")
        report.append("This report provides a complete structural analysis of the W3_HB_team_BXCGICOG repository.")
        report.append("")
        report.append("### Category Summary")
        report.append("")
        report.append("| Category | Item Count |")
        report.append("|----------|------------|")
        for category, items in self.categories.items():
            if items and items[0] != '.':
                report.append(f"| {category.replace('_', ' ').title()} | {len(items)} |")
        report.append("")
        report.append("---")
        report.append("")
        
        # Core System
        report.append("## 🏛️ Core System")
        report.append("")
        report.append("**Classification:** KEEP")
        report.append("")
        report.append("Essential system components that define the W3 architecture.")
        report.append("")
        if self.categories['core_system']:
            for item in sorted(self.categories['core_system']):
                if item != '.':
                    report.append(f"- `{item}`")
        else:
            report.append("*No core system directories found*")
        report.append("")
        report.append("---")
        report.append("")
        
        # W3Lgu
        report.append("## 🗣️ W3Lgu")
        report.append("")
        report.append("**Classification:** KEEP")
        report.append("")
        report.append("W3 Language Unit - The internal language system.")
        report.append("")
        if self.categories['w3lgu']:
            for item in sorted(self.categories['w3lgu']):
                if item != '.':
                    report.append(f"- `{item}`")
        else:
            report.append("*No W3Lgu directories found*")
        report.append("")
        report.append("---")
        report.append("")
        
        # Modules
        report.append("## 🤖 AI Modules")
        report.append("")
        report.append("**Classification:** KEEP")
        report.append("")
        report.append("Core AI team members and their workspaces.")
        report.append("")
        if self.categories['modules']:
            # Group by module
            modules = {}
            for item in self.categories['modules']:
                if item != '.':
                    # Extract module name
                    parts = item.split('/')
                    if parts:
                        module_name = parts[0]
                        if module_name not in modules:
                            modules[module_name] = []
                        modules[module_name].append(item)
            
            for module, paths in sorted(modules.items()):
                report.append(f"### {module.upper()}")
                report.append("")
                for path in sorted(paths)[:10]:  # Limit to first 10
                    report.append(f"- `{path}`")
                if len(paths) > 10:
                    report.append(f"- *(... and {len(paths) - 10} more)*")
                report.append("")
        else:
            report.append("*No module directories found*")
        report.append("")
        report.append("---")
        report.append("")
        
        # Docs / PWA
        report.append("## 📚 Documentation & PWA")
        report.append("")
        report.append("**Classification:** KEEP")
        report.append("")
        report.append("Documentation, branding, and metadata.")
        report.append("")
        if self.categories['docs_pwa']:
            for item in sorted(self.categories['docs_pwa']):
                if item != '.':
                    report.append(f"- `{item}`")
        else:
            report.append("*No documentation directories found*")
        report.append("")
        report.append("---")
        report.append("")
        
        # Experimental
        report.append("## 🧪 Experimental / Lab")
        report.append("")
        report.append("**Classification:** REVIEW")
        report.append("")
        report.append("Experimental features, prototypes, and testing grounds.")
        report.append("")
        if self.categories['experimental']:
            for item in sorted(self.categories['experimental'])[:15]:  # Limit display
                if item != '.':
                    report.append(f"- `{item}`")
            if len(self.categories['experimental']) > 15:
                report.append(f"- *(... and {len(self.categories['experimental']) - 15} more)*")
        else:
            report.append("*No experimental directories found*")
        report.append("")
        report.append("---")
        report.append("")
        
        # Deprecated
        report.append("## 🗑️ Deprecated")
        report.append("")
        report.append("**Classification:** DEPRECATE")
        report.append("")
        report.append("Legacy directories that should not be used.")
        report.append("")
        if self.categories['deprecated']:
            for item in sorted(self.categories['deprecated']):
                if item != '.':
                    report.append(f"- `{item}` ⚠️ **DO NOT USE**")
        else:
            report.append("✅ *No deprecated directories found*")
        report.append("")
        report.append("---")
        report.append("")
        
        # Case Sensitivity Issues
        report.append("## 🔤 Case Sensitivity Check")
        report.append("")
        if self.case_issues:
            report.append(f"⚠️ **{len(self.case_issues)} potential issue(s) detected**")
            report.append("")
            for i, issue in enumerate(self.case_issues, 1):
                report.append(f"### Issue #{i}")
                report.append(f"- **Type:** {issue['type'].title()}")
                report.append(f"- **Path 1:** `{issue['path1']}`")
                report.append(f"- **Path 2:** `{issue['path2']}`")
                report.append(f"- **Issue:** {issue['issue']}")
                report.append("")
        else:
            report.append("✅ No case sensitivity issues detected")
        report.append("")
        report.append("---")
        report.append("")
        
        # Ghost Folders
        report.append("## 👻 Ghost Folders")
        report.append("")
        if self.empty_folders:
            report.append(f"**Total:** {len(self.empty_folders)} empty folders")
            report.append("")
            report.append("| Path | Reason |")
            report.append("|------|--------|")
            for folder in self.empty_folders:
                report.append(f"| `{folder['path']}` | {folder['reason']} |")
        else:
            report.append("✅ No ghost folders detected")
        report.append("")
        report.append("---")
        report.append("")
        
        # Recommendations
        report.append("## 📋 Classification Summary")
        report.append("")
        report.append("### KEEP")
        report.append("- Core System")
        report.append("- W3Lgu")
        report.append("- AI Modules (ChatGPT, Gemini, Grok, DeepSeek, Copilot-Gm, BBX19)")
        report.append("- Documentation & PWA")
        report.append("- Tools")
        report.append("")
        report.append("### REVIEW")
        report.append("- Experimental directories")
        report.append("- Lab/Studio spaces")
        report.append("- Prototype folders")
        report.append("")
        report.append("### DEPRECATE")
        report.append("- Old `Copilot/` directory (use `Copilot-Gm/` instead)")
        report.append("- Any directories marked as deprecated in README")
        report.append("")
        report.append("---")
        report.append("")
        
        # Footer
        report.append("## 📌 Notes")
        report.append("")
        report.append("- This map reflects the current state of the repository")
        report.append("- Classifications are based on naming conventions and location")
        report.append("- Empty folders with .gitkeep are intentional placeholders")
        report.append("- Case sensitivity issues may cause problems on different operating systems")
        report.append("")
        report.append("---")
        report.append("")
        report.append("**Generated by:** REDR (Reader)  ")
        report.append("**Authority:** BBX19 — Root Authority  ")
        report.append("**System:** W3 Security & Structural Audit")
        
        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"📄 Report saved to: {output_path}")


def main():
    """Main execution"""
    repo_path = Path(__file__).parent.parent
    reader = REDRReader(repo_path)
    
    # Run structure scan
    reader.scan_structure()
    
    # Generate report
    report_path = repo_path / 'REDR_Structure_Map.md'
    reader.generate_report(report_path)


if __name__ == '__main__':
    main()

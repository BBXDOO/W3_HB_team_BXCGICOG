#!/usr/bin/env python3
"""
File Integrity Check Tool
Checks for missing, corrupted, or damaged files in the W3_HB_team_BXCGICOG repository
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

class FileIntegrityChecker:
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.issues = {
            "missing_directories": [],
            "missing_files": [],
            "corrupted_json": [],
            "empty_files_suspicious": [],
            "broken_symlinks": []
        }
        
    def check_module_dependencies(self):
        """Check if directories and files referenced in module.json exist"""
        # Dynamically discover all module.json files
        module_files = []
        for json_file in self.repo_root.rglob("module.json"):
            if '.git' not in json_file.parts:
                rel_path = json_file.relative_to(self.repo_root)
                module_files.append(str(rel_path))
        
        for module_file in module_files:
            module_path = self.repo_root / module_file
            if not module_path.exists():
                self.issues["missing_files"].append(str(module_file))
                continue
                
            try:
                with open(module_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Check input paths
                if 'input' in data:
                    for input_path in data['input']:
                        if '*' in input_path:  # Skip wildcard paths
                            continue
                        full_path = self.repo_root / input_path
                        if not full_path.exists():
                            self.issues["missing_directories" if input_path.endswith('/') else "missing_files"].append(input_path)
                
                # Check output paths
                if 'output' in data:
                    for output_path in data['output']:
                        if '*' in output_path:  # Skip wildcard paths
                            continue
                        full_path = self.repo_root / output_path
                        if not full_path.exists():
                            self.issues["missing_directories" if output_path.endswith('/') else "missing_files"].append(output_path)
                            
            except json.JSONDecodeError as e:
                self.issues["corrupted_json"].append(f"{module_file}: {str(e)}")
    
    def check_json_integrity(self):
        """Check all JSON files for corruption"""
        for json_file in self.repo_root.rglob("*.json"):
            # Skip .git directory
            if '.git' in json_file.parts:
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                rel_path = json_file.relative_to(self.repo_root)
                self.issues["corrupted_json"].append(f"{rel_path}: Line {e.lineno}, Column {e.colno}")
            except Exception as e:
                rel_path = json_file.relative_to(self.repo_root)
                self.issues["corrupted_json"].append(f"{rel_path}: {str(e)}")
    
    def check_empty_files(self):
        """Check for suspicious empty files (excluding .gitkeep)"""
        for file_path in self.repo_root.rglob("*"):
            if not file_path.is_file():
                continue
            if '.git' in file_path.parts:
                continue
            if file_path.name == '.gitkeep':
                continue
                
            if file_path.stat().st_size == 0:
                rel_path = file_path.relative_to(self.repo_root)
                self.issues["empty_files_suspicious"].append(str(rel_path))
    
    def check_broken_symlinks(self):
        """Check for broken symbolic links"""
        for link_path in self.repo_root.rglob("*"):
            if link_path.is_symlink() and not link_path.exists():
                rel_path = link_path.relative_to(self.repo_root)
                self.issues["broken_symlinks"].append(str(rel_path))
    
    def run_all_checks(self):
        """Run all integrity checks"""
        print("Running file integrity checks...")
        self.check_module_dependencies()
        self.check_json_integrity()
        self.check_empty_files()
        self.check_broken_symlinks()
    
    def generate_report(self):
        """Generate a detailed report"""
        report = []
        report.append("=" * 80)
        report.append("FILE INTEGRITY CHECK REPORT")
        report.append("=" * 80)
        report.append(f"Repository: W3_HB_team_BXCGICOG")
        report.append(f"Check Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        report.append("")
        
        total_issues = sum(len(v) for v in self.issues.values())
        
        if total_issues == 0:
            report.append("✅ STATUS: ALL CHECKS PASSED")
            report.append("No missing, corrupted, or damaged files detected.")
        else:
            report.append(f"⚠️  STATUS: {total_issues} ISSUES DETECTED")
        
        report.append("")
        
        # Missing directories
        if self.issues["missing_directories"]:
            report.append("📁 MISSING DIRECTORIES:")
            report.append("-" * 40)
            for item in sorted(set(self.issues["missing_directories"])):
                report.append(f"  • {item}")
            report.append("")
        
        # Missing files
        if self.issues["missing_files"]:
            report.append("📄 MISSING FILES:")
            report.append("-" * 40)
            for item in sorted(set(self.issues["missing_files"])):
                report.append(f"  • {item}")
            report.append("")
        
        # Corrupted JSON
        if self.issues["corrupted_json"]:
            report.append("⚠️  CORRUPTED JSON FILES:")
            report.append("-" * 40)
            for item in sorted(set(self.issues["corrupted_json"])):
                report.append(f"  • {item}")
            report.append("")
        
        # Empty files
        if self.issues["empty_files_suspicious"]:
            report.append("🔍 SUSPICIOUS EMPTY FILES:")
            report.append("-" * 40)
            for item in sorted(set(self.issues["empty_files_suspicious"])):
                report.append(f"  • {item}")
            report.append("")
        
        # Broken symlinks
        if self.issues["broken_symlinks"]:
            report.append("🔗 BROKEN SYMBOLIC LINKS:")
            report.append("-" * 40)
            for item in sorted(set(self.issues["broken_symlinks"])):
                report.append(f"  • {item}")
            report.append("")
        
        report.append("=" * 80)
        report.append("SUMMARY:")
        report.append("-" * 40)
        report.append(f"Missing Directories:     {len(set(self.issues['missing_directories']))}")
        report.append(f"Missing Files:           {len(set(self.issues['missing_files']))}")
        report.append(f"Corrupted JSON Files:    {len(set(self.issues['corrupted_json']))}")
        report.append(f"Suspicious Empty Files:  {len(set(self.issues['empty_files_suspicious']))}")
        report.append(f"Broken Symbolic Links:   {len(set(self.issues['broken_symlinks']))}")
        report.append(f"TOTAL ISSUES:            {total_issues}")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def get_issues_dict(self):
        """Return issues as a dictionary"""
        return self.issues


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    checker = FileIntegrityChecker(repo_root)
    checker.run_all_checks()
    
    report = checker.generate_report()
    print(report)
    
    # Save report to file
    report_file = os.path.join(repo_root, "tools", "file_integrity_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_file}")
    
    # Return exit code based on issues found
    total_issues = sum(len(v) for v in checker.get_issues_dict().values())
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

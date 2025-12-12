#!/usr/bin/env python3
"""
Module Validation Tool
Validates all module.json files for completeness and correctness
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class ModuleValidator:
    REQUIRED_FIELDS = ["name", "display_name", "version", "owner", "input", "output", "scope"]
    OPTIONAL_FIELDS = ["lifecycle", "contact", "notes", "confidence_policy", "pattern_weight"]
    
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.results = {
            "valid_modules": [],
            "invalid_modules": [],
            "warnings": []
        }
    
    def find_module_files(self) -> List[Path]:
        """Find all module.json files"""
        module_files = []
        for module_file in self.repo_root.rglob("module.json"):
            if '.git' not in module_file.parts:
                module_files.append(module_file)
        return module_files
    
    def validate_module(self, module_path: Path) -> Tuple[bool, List[str]]:
        """Validate a single module.json file"""
        errors = []
        
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"JSON parsing error: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"Error reading file: {e}")
            return False, errors
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Validate field types
        if "input" in data and not isinstance(data["input"], list):
            errors.append("Field 'input' must be an array")
        
        if "output" in data and not isinstance(data["output"], list):
            errors.append("Field 'output' must be an array")
        
        # Check version format (basic semver validation)
        if "version" in data:
            version = data["version"]
            if not isinstance(version, str):
                errors.append(f"Invalid version format: {version}. Expected string.")
            elif not self._is_valid_semver(version):
                errors.append(f"Invalid version format: {version}. Expected semver format (e.g., 1.0.0, 1.0.0-alpha, 2.1.0-beta.1)")
        
        return len(errors) == 0, errors
    
    def _is_valid_semver(self, version: str) -> bool:
        """Basic semver validation (supports X.Y.Z and X.Y.Z-prerelease)"""
        import re
        # Simplified semver pattern: major.minor.patch with optional prerelease
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$'
        return re.match(pattern, version) is not None
    
    def run_validation(self):
        """Run validation on all module files"""
        module_files = self.find_module_files()
        
        if not module_files:
            print("No module.json files found.")
            return
        
        for module_file in module_files:
            rel_path = module_file.relative_to(self.repo_root)
            is_valid, errors = self.validate_module(module_file)
            
            if is_valid:
                self.results["valid_modules"].append(str(rel_path))
            else:
                self.results["invalid_modules"].append((str(rel_path), errors))
    
    def generate_report(self):
        """Generate validation report"""
        report = []
        report.append("=" * 80)
        report.append("MODULE VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Valid modules
        if self.results["valid_modules"]:
            report.append(f"✅ VALID MODULES ({len(self.results['valid_modules'])}):")
            report.append("-" * 40)
            for module in sorted(self.results["valid_modules"]):
                report.append(f"  • {module}")
            report.append("")
        
        # Invalid modules
        if self.results["invalid_modules"]:
            report.append(f"❌ INVALID MODULES ({len(self.results['invalid_modules'])}):")
            report.append("-" * 40)
            for module, errors in self.results["invalid_modules"]:
                report.append(f"  • {module}")
                for error in errors:
                    report.append(f"    - {error}")
            report.append("")
        
        # Warnings
        if self.results["warnings"]:
            report.append(f"⚠️  WARNINGS ({len(self.results['warnings'])}):")
            report.append("-" * 40)
            for warning in self.results["warnings"]:
                report.append(f"  • {warning}")
            report.append("")
        
        # Summary
        report.append("=" * 80)
        report.append("SUMMARY:")
        report.append("-" * 40)
        report.append(f"Valid Modules:    {len(self.results['valid_modules'])}")
        report.append(f"Invalid Modules:  {len(self.results['invalid_modules'])}")
        report.append(f"Warnings:         {len(self.results['warnings'])}")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    import os
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    validator = ModuleValidator(repo_root)
    
    print("Running module validation...")
    validator.run_validation()
    
    report = validator.generate_report()
    print(report)
    
    # Return exit code
    return 1 if validator.results["invalid_modules"] else 0

if __name__ == "__main__":
    sys.exit(main())

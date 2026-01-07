#!/usr/bin/env python3
"""
JSON Schema Validation Tool
Validates JSON data files against their corresponding schema files
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import jsonschema
    from jsonschema import validate, ValidationError, SchemaError
except ImportError:
    print("Error: jsonschema library is not installed.")
    print("Please install it using: pip install jsonschema")
    sys.exit(1)

class JSONSchemaValidator:
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.results = {
            "validated": [],
            "failed": [],
            "warnings": []
        }
        
    def find_schema_files(self):
        """Find all .schema.json files"""
        schema_files = []
        for schema_file in self.repo_root.rglob("*.schema.json"):
            if '.git' not in schema_file.parts and 'node_modules' not in schema_file.parts:
                schema_files.append(schema_file)
        return schema_files
    
    def validate_pair(self, schema_path: Path, data_path: Path) -> Tuple[bool, str]:
        """Validate a data file against its schema"""
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            validate(instance=data, schema=schema)
            return True, ""
        except ValidationError as e:
            return False, f"Validation error: {e.message}"
        except SchemaError as e:
            return False, f"Schema error: {e.message}"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def run_validation(self):
        """Run validation on all schema/data pairs"""
        schema_files = self.find_schema_files()
        
        if not schema_files:
            print("No schema files found.")
            return
        
        for schema_file in schema_files:
            # Derive data file path
            data_file = schema_file.parent / schema_file.name.replace('.schema.json', '.json')
            
            rel_schema = schema_file.relative_to(self.repo_root)
            rel_data = data_file.relative_to(self.repo_root) if data_file.exists() else None
            
            if not data_file.exists():
                self.results["warnings"].append(f"Schema {rel_schema} has no matching data file")
                continue
            
            is_valid, error = self.validate_pair(schema_file, data_file)
            
            if is_valid:
                self.results["validated"].append(str(rel_data))
            else:
                self.results["failed"].append((str(rel_data), str(rel_schema), error))
    
    def generate_report(self):
        """Generate validation report"""
        report = []
        report.append("=" * 80)
        report.append("JSON SCHEMA VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Validated files
        if self.results["validated"]:
            report.append(f"✅ VALIDATED FILES ({len(self.results['validated'])}):")
            report.append("-" * 40)
            for file in self.results["validated"]:
                report.append(f"  • {file}")
            report.append("")
        
        # Failed validations
        if self.results["failed"]:
            report.append(f"❌ FAILED VALIDATIONS ({len(self.results['failed'])}):")
            report.append("-" * 40)
            for data_file, schema_file, error in self.results["failed"]:
                report.append(f"  • {data_file}")
                report.append(f"    Schema: {schema_file}")
                report.append(f"    Error: {error}")
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
        report.append(f"Validated:  {len(self.results['validated'])}")
        report.append(f"Failed:     {len(self.results['failed'])}")
        report.append(f"Warnings:   {len(self.results['warnings'])}")
        report.append("=" * 80)
        
        return "\n".join(report)

def main():
    import os
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    validator = JSONSchemaValidator(repo_root)
    
    print("Running JSON schema validation...")
    validator.run_validation()
    
    report = validator.generate_report()
    print(report)
    
    # Return exit code
    return 1 if validator.results["failed"] else 0

if __name__ == "__main__":
    sys.exit(main())

# File Integrity Check Tools

This directory contains tools for checking file integrity, validating JSON schemas, and verifying module definitions in the W3_HB_team_BXCGICOG repository.

## Dependencies

- Python 3.x (pre-installed)
- jsonschema library (required for JSON schema validation)

**Install dependencies:**
```bash
pip install jsonschema
```

## Tools

### 1. file_integrity_check.py

A comprehensive file integrity checker that validates:
- Missing directories referenced in module.json files
- Missing files
- Corrupted JSON files
- Suspicious empty files (excluding .gitkeep)
- Broken symbolic links

**Usage:**
```bash
python3 tools/file_integrity_check.py
```

**Output:**
- Console output with detailed report
- Report file saved to `tools/file_integrity_report.txt`

**Exit Code:**
- `0` - No issues found
- `1` - Issues detected

### 2. validate_json_schemas.py

Validates JSON data files against their corresponding JSON Schema definitions using Python's jsonschema library. Supports all JSON Schema versions including 2020-12.

**Requirements:**
```bash
pip install jsonschema
```

**Usage:**
```bash
python3 tools/validate_json_schemas.py
```

**Features:**
- Automatically finds all .schema.json files
- Validates corresponding .json data files
- Reports validation errors with detailed messages
- Supports JSON Schema draft 2020-12 and earlier versions

**Exit Code:**
- `0` - All validations passed
- `1` - One or more validations failed

### 3. validate_modules.py

Validates all module.json files for completeness and correctness according to the W3 module schema.

**Usage:**
```bash
python3 tools/validate_modules.py
```

**Validates:**
- Required fields: name, display_name, version, owner, input, output, scope
- Optional fields: lifecycle, contact, notes, confidence_policy, pattern_weight
- Field types (arrays for input/output)
- Version format (semver)

**Exit Code:**
- `0` - All modules valid
- `1` - One or more modules invalid

### 4. validate_metadata.py

Validates metadata fields in markdown files according to W3 governance rules.

**Usage:**
```bash
python3 tools/validate_metadata.py
```

**Validates:**
- If 'approved-by' is present, 'reason' must also be present

**Exit Code:**
- `0` - All metadata valid
- `1` - Validation errors found

### 5. send_integrity_report.py

Email notification script that sends the file integrity report via email.

**Usage:**
```bash
# Set environment variables
export SENDER_EMAIL="your-email@example.com"
export RECIPIENT_EMAIL="recipient@example.com"
export SENDER_PASSWORD="your-app-password"

# Optional: Configure SMTP server (defaults to Gmail)
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export USE_TLS="true"

# Run the script
python3 tools/send_integrity_report.py
```

**Features:**
- Runs integrity check automatically
- Generates both plain text and HTML formatted reports
- Sends email with comprehensive issue details
- Falls back to file output if email configuration is incomplete

**Email Configuration:**

For Gmail:
1. Enable 2-factor authentication on your Google account
2. Generate an app password at https://myaccount.google.com/apppasswords
3. Use the app password as SENDER_PASSWORD

For other SMTP servers, adjust SMTP_SERVER and SMTP_PORT accordingly.

## Report Format

The reports include:

### 📁 Missing Directories
Directories that should exist based on module.json configuration but are not present.

### 📄 Missing Files
Files that are referenced but cannot be found.

### ⚠️ Corrupted JSON Files
JSON files that fail to parse or have syntax errors.

### 🔍 Suspicious Empty Files
Files that are empty (excluding .gitkeep files which are intentionally empty).

### 🔗 Broken Symbolic Links
Symbolic links that point to non-existent targets.

## Current Status

As of the last W3 Full Sanity Sweep (2025-12-12):

✅ **All checks passed:**
- Missing Directories: 0
- Missing Files: 0
- Corrupted JSON Files: 0
- Suspicious Empty Files: 0
- Broken Symbolic Links: 0
- Valid Modules: 7/7
- JSON Schema Validations: 2/2

## Full Sanity Sweep

Run a comprehensive validation of the entire repository:

```bash
# 1. File integrity
python3 tools/file_integrity_check.py

# 2. JSON schema validation
python3 tools/validate_json_schemas.py

# 3. Module validation
python3 tools/validate_modules.py

# 4. Metadata validation
python3 tools/validate_metadata.py
```

Or use the one-liner:
```bash
python3 tools/file_integrity_check.py && \
python3 tools/validate_json_schemas.py && \
python3 tools/validate_modules.py && \
python3 tools/validate_metadata.py && \
echo "✅ Full Sanity Sweep: ALL CHECKS PASSED"
```

## Integration

These tools can be integrated into:
- CI/CD pipelines for automated checks
- Pre-commit hooks
- Scheduled cron jobs for periodic monitoring
- GitHub Actions workflows

## Example GitHub Actions Workflow

The repository includes a GitHub Actions workflow at `.github/workflows/validate-json.yml` that:
1. Validates JSON syntax for all JSON files
2. Validates JSON data files against their schemas using the Python validator

## Notes

- The checker validates against the structure defined in module.json files
- Wildcard paths (containing '*') are intentionally skipped
- .gitkeep files are excluded from empty file checks as they are intentionally empty
- The .git directory is excluded from all checks
- Python jsonschema library supports all JSON Schema versions including 2020-12

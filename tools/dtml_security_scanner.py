#!/usr/bin/env python3
"""
DTML (Detection Manual) - Security Scanner
Role: Gatekeeper / Stop-the-world Authority
Priority: CRITICAL

Scans for:
- API Keys / Tokens / Secrets
- Recent commits (48 hours)
- Risky files (scripts, configs, env)
"""

import os
import re
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Common patterns for secrets
SECRET_PATTERNS = [
    # API Keys and Tokens
    (r'api[_-]?key[\s]*[:=][\s]*[\'"]?([a-zA-Z0-9_\-]{20,})[\'"]?', 'API Key'),
    (r'token[\s]*[:=][\s]*[\'"]?([a-zA-Z0-9_\-]{20,})[\'"]?', 'Token'),
    (r'secret[\s]*[:=][\s]*[\'"]?([a-zA-Z0-9_\-]{20,})[\'"]?', 'Secret'),
    (r'password[\s]*[:=][\s]*[\'"]?([a-zA-Z0-9_\-]{8,})[\'"]?', 'Password'),
    (r'credential[\s]*[:=][\s]*[\'"]?([a-zA-Z0-9_\-]{10,})[\'"]?', 'Credential'),
    
    # AWS Keys
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key'),
    (r'aws[_-]?secret[_-]?access[_-]?key[\s]*[:=][\s]*[\'"]?([a-zA-Z0-9/+=]{40})[\'"]?', 'AWS Secret Key'),
    
    # GitHub Tokens
    (r'gh[ps]_[a-zA-Z0-9]{36,}', 'GitHub Token'),
    
    # Generic tokens
    (r'["\']?[a-zA-Z0-9_-]*token["\']?\s*[:=]\s*["\']([a-zA-Z0-9_\-]{20,})["\']', 'Generic Token'),
    
    # Private keys
    (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----', 'Private Key'),
]

# Risky file patterns
RISKY_EXTENSIONS = ['.env', '.key', '.pem', '.p12', '.pfx', '.sh', '.bat', '.cmd']
RISKY_FILENAMES = ['credentials', 'secrets', 'password', 'config', '.npmrc', '.pypirc']

# Exclude patterns
EXCLUDE_DIRS = ['.git', 'node_modules', '__pycache__', '.venv', 'venv']
EXCLUDE_FILES = ['package-lock.json', '*.min.js', '*.map']


class DTMLScanner:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.findings = []
        self.risky_files = []
        self.recent_commits = []
        self.status = "SAFE"
        
    def should_exclude(self, path):
        """Check if path should be excluded from scanning"""
        path_str = str(path)
        for exclude_dir in EXCLUDE_DIRS:
            if f'/{exclude_dir}/' in path_str or path_str.endswith(f'/{exclude_dir}'):
                return True
        return False
    
    def scan_file_for_secrets(self, file_path):
        """Scan a single file for secrets"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            line_number = 0
            for line in content.split('\n'):
                line_number += 1
                for pattern, secret_type in SECRET_PATTERNS:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Avoid false positives from documentation
                        if 'example' in line.lower() or 'placeholder' in line.lower():
                            continue
                        if 'your-' in line.lower() or 'my-' in line.lower():
                            continue
                        if 'xxx' in match.group(0).lower():
                            continue
                            
                        self.findings.append({
                            'type': secret_type,
                            'file': str(file_path.relative_to(self.repo_path)),
                            'line': line_number,
                            'context': line.strip()[:100]
                        })
                        self.status = "RISK"
        except Exception as e:
            pass
    
    def find_risky_files(self):
        """Find files with risky extensions or names"""
        for root, dirs, files in os.walk(self.repo_path):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                
                # Check for risky extensions
                if any(file.endswith(ext) for ext in RISKY_EXTENSIONS):
                    self.risky_files.append({
                        'path': str(file_path.relative_to(self.repo_path)),
                        'reason': 'Risky extension',
                        'type': 'extension'
                    })
                
                # Check for risky filenames
                if any(risky in file.lower() for risky in RISKY_FILENAMES):
                    self.risky_files.append({
                        'path': str(file_path.relative_to(self.repo_path)),
                        'reason': 'Risky filename',
                        'type': 'filename'
                    })
    
    def scan_recent_commits(self):
        """Scan commits from the last 48 hours"""
        try:
            # Get commits from last 48 hours
            cutoff_time = datetime.now() - timedelta(hours=48)
            cutoff_str = cutoff_time.strftime('%Y-%m-%d %H:%M:%S')
            
            result = subprocess.run(
                ['git', 'log', '--all', '--since', cutoff_str, '--pretty=format:%H|%an|%s|%ad'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 4:
                            commit_hash, author, message, date = parts[0], parts[1], parts[2], parts[3]
                            self.recent_commits.append({
                                'hash': commit_hash[:8],
                                'author': author,
                                'message': message,
                                'date': date
                            })
        except Exception as e:
            pass
    
    def scan_all_files(self):
        """Scan all files in repository"""
        for root, dirs, files in os.walk(self.repo_path):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                if not self.should_exclude(file_path):
                    self.scan_file_for_secrets(file_path)
    
    def run_scan(self):
        """Execute complete security scan"""
        print("🛡️  DTML Security Scanner Starting...")
        print(f"📂 Repository: {self.repo_path}")
        print()
        
        # 1. Scan for secrets
        print("🔍 Scanning for secrets and credentials...")
        self.scan_all_files()
        print(f"   Found {len(self.findings)} potential secret(s)")
        
        # 2. Find risky files
        print("⚠️  Identifying risky files...")
        self.find_risky_files()
        print(f"   Found {len(self.risky_files)} risky file(s)")
        
        # 3. Check recent commits
        print("📝 Checking recent commits (48 hours)...")
        self.scan_recent_commits()
        print(f"   Found {len(self.recent_commits)} recent commit(s)")
        
        # Determine final status
        if len(self.findings) > 0:
            self.status = "BLOCK"
        elif len(self.risky_files) > 5:
            self.status = "RISK"
        
        print()
        print(f"✅ Scan complete. Status: {self.status}")
        return self.status
    
    def generate_report(self, output_path):
        """Generate detailed security report"""
        report = []
        report.append("# DTML Security Scan Report")
        report.append("")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Status:** {self.status}")
        report.append("")
        report.append("---")
        report.append("")
        
        # Status Legend
        report.append("## 🚦 Status Legend")
        report.append("")
        report.append("- **SAFE** — No security risks detected")
        report.append("- **RISK** — Potential risks found, review recommended")
        report.append("- **BLOCK** — Critical risks detected, merge blocked")
        report.append("")
        report.append("---")
        report.append("")
        
        # Recent Commits
        report.append("## 📝 Recent Commits (48 hours)")
        report.append("")
        if self.recent_commits:
            report.append(f"**Total:** {len(self.recent_commits)} commits")
            report.append("")
            report.append("| Hash | Author | Message | Date |")
            report.append("|------|--------|---------|------|")
            for commit in self.recent_commits:
                report.append(f"| `{commit['hash']}` | {commit['author']} | {commit['message'][:50]} | {commit['date'][:19]} |")
        else:
            report.append("✅ No commits in the last 48 hours")
        report.append("")
        report.append("---")
        report.append("")
        
        # Secret Findings
        report.append("## 🔐 Secret Detection Results")
        report.append("")
        if self.findings:
            report.append(f"⚠️ **{len(self.findings)} potential secret(s) detected**")
            report.append("")
            for i, finding in enumerate(self.findings, 1):
                report.append(f"### Finding #{i}: {finding['type']}")
                report.append(f"- **File:** `{finding['file']}`")
                report.append(f"- **Line:** {finding['line']}")
                report.append(f"- **Context:** `{finding['context']}`")
                report.append("")
        else:
            report.append("✅ No secrets or credentials detected")
        report.append("")
        report.append("---")
        report.append("")
        
        # Risky Files
        report.append("## ⚠️ Risky Files")
        report.append("")
        if self.risky_files:
            report.append(f"**Total:** {len(self.risky_files)} risky files")
            report.append("")
            
            # Group by type
            by_extension = [f for f in self.risky_files if f['type'] == 'extension']
            by_filename = [f for f in self.risky_files if f['type'] == 'filename']
            
            if by_extension:
                report.append("### Risky Extensions")
                for file in by_extension:
                    report.append(f"- `{file['path']}`")
                report.append("")
            
            if by_filename:
                report.append("### Risky Filenames")
                for file in by_filename:
                    report.append(f"- `{file['path']}`")
                report.append("")
        else:
            report.append("✅ No risky files detected")
        report.append("")
        report.append("---")
        report.append("")
        
        # Recommendations
        report.append("## 📋 Recommendations")
        report.append("")
        if self.status == "BLOCK":
            report.append("### 🚫 BLOCKED")
            report.append("- **Action:** Do NOT merge")
            report.append("- **Reason:** Critical security risks detected")
            report.append("- **Next Steps:**")
            report.append("  1. Remove all detected secrets immediately")
            report.append("  2. Rotate compromised credentials")
            report.append("  3. Re-run security scan")
            report.append("  4. Update .gitignore to prevent future leaks")
        elif self.status == "RISK":
            report.append("### ⚠️ RISK")
            report.append("- **Action:** Review before merge")
            report.append("- **Reason:** Potential security concerns")
            report.append("- **Next Steps:**")
            report.append("  1. Review all risky files")
            report.append("  2. Ensure no secrets in configuration files")
            report.append("  3. Consider using environment variables")
        else:
            report.append("### ✅ SAFE")
            report.append("- **Action:** Proceed with caution")
            report.append("- **Note:** Continue following security best practices")
        report.append("")
        report.append("---")
        report.append("")
        
        # Footer
        report.append("## 📌 Notes")
        report.append("")
        report.append("- This scan checks the last 48 hours of commits")
        report.append("- False positives may occur in documentation or example files")
        report.append("- Always verify findings manually before taking action")
        report.append("- Risky files are flagged for review, not necessarily problematic")
        report.append("")
        report.append("---")
        report.append("")
        report.append("**Generated by:** DTML (Detection Manual)  ")
        report.append("**Authority:** BBX19 — Root Authority  ")
        report.append("**System:** W3 Security & Structural Audit")
        
        # Write report
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"📄 Report saved to: {output_path}")


def main():
    """Main execution"""
    repo_path = Path(__file__).parent.parent
    scanner = DTMLScanner(repo_path)
    
    # Run scan
    status = scanner.run_scan()
    
    # Generate report
    report_path = repo_path / 'DTML_Report.md'
    scanner.generate_report(report_path)
    
    # Exit with status code
    if status == "BLOCK":
        exit(1)
    elif status == "RISK":
        exit(0)
    else:
        exit(0)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Email Notification Script for File Integrity Report
Sends the file integrity check report via email
"""

import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

# Import the checker
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from file_integrity_check import FileIntegrityChecker


class EmailReporter:
    def __init__(self, config_file=None):
        self.config = self.load_config(config_file)
        
    def load_config(self, config_file):
        """Load email configuration from file or environment variables"""
        default_config = {
            "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": int(os.getenv("SMTP_PORT", "587")),
            "sender_email": os.getenv("SENDER_EMAIL", ""),
            "sender_password": os.getenv("SENDER_PASSWORD", ""),
            "recipient_email": os.getenv("RECIPIENT_EMAIL", ""),
            "use_tls": os.getenv("USE_TLS", "true").lower() == "true"
        }
        
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                default_config.update(file_config)
        
        return default_config
    
    def create_html_report(self, checker):
        """Create an HTML formatted email report"""
        issues = checker.get_issues_dict()
        
        # Deduplicate all issues once
        deduped_issues = {
            key: sorted(set(values)) for key, values in issues.items()
        }
        
        total_issues = sum(len(v) for v in deduped_issues.values())
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #f4f4f4; padding: 20px; border-left: 5px solid #007bff; }}
                .status-ok {{ color: #28a745; font-weight: bold; }}
                .status-warning {{ color: #ffc107; font-weight: bold; }}
                .status-error {{ color: #dc3545; font-weight: bold; }}
                .section {{ margin: 20px 0; padding: 15px; background-color: #f9f9f9; border-radius: 5px; }}
                .section-title {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #007bff; }}
                .issue-list {{ list-style-type: none; padding-left: 0; }}
                .issue-list li {{ padding: 5px 0; padding-left: 20px; }}
                .issue-list li:before {{ content: "• "; color: #dc3545; font-weight: bold; }}
                .summary {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-top: 20px; }}
                .summary-item {{ padding: 5px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔍 File Integrity Check Report</h1>
                <p><strong>Repository:</strong> W3_HB_team_BXCGICOG</p>
                <p><strong>Check Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        if total_issues == 0:
            html += """
            <div class="section">
                <p class="status-ok">✅ STATUS: ALL CHECKS PASSED</p>
                <p>No missing, corrupted, or damaged files detected.</p>
            </div>
            """
        else:
            html += f"""
            <div class="section">
                <p class="status-error">⚠️ STATUS: {total_issues} ISSUES DETECTED</p>
            </div>
            """
            
            if deduped_issues["missing_directories"]:
                html += """
                <div class="section">
                    <div class="section-title">📁 Missing Directories</div>
                    <ul class="issue-list">
                """
                for item in deduped_issues["missing_directories"]:
                    html += f"<li>{item}</li>"
                html += "</ul></div>"
            
            if deduped_issues["missing_files"]:
                html += """
                <div class="section">
                    <div class="section-title">📄 Missing Files</div>
                    <ul class="issue-list">
                """
                for item in deduped_issues["missing_files"]:
                    html += f"<li>{item}</li>"
                html += "</ul></div>"
            
            if deduped_issues["corrupted_json"]:
                html += """
                <div class="section">
                    <div class="section-title">⚠️ Corrupted JSON Files</div>
                    <ul class="issue-list">
                """
                for item in deduped_issues["corrupted_json"]:
                    html += f"<li>{item}</li>"
                html += "</ul></div>"
            
            if deduped_issues["empty_files_suspicious"]:
                html += """
                <div class="section">
                    <div class="section-title">🔍 Suspicious Empty Files</div>
                    <ul class="issue-list">
                """
                for item in deduped_issues["empty_files_suspicious"]:
                    html += f"<li>{item}</li>"
                html += "</ul></div>"
            
            if deduped_issues["broken_symlinks"]:
                html += """
                <div class="section">
                    <div class="section-title">🔗 Broken Symbolic Links</div>
                    <ul class="issue-list">
                """
                for item in deduped_issues["broken_symlinks"]:
                    html += f"<li>{item}</li>"
                html += "</ul></div>"
        
        html += f"""
            <div class="summary">
                <h2>Summary</h2>
                <div class="summary-item"><strong>Missing Directories:</strong> {len(deduped_issues['missing_directories'])}</div>
                <div class="summary-item"><strong>Missing Files:</strong> {len(deduped_issues['missing_files'])}</div>
                <div class="summary-item"><strong>Corrupted JSON Files:</strong> {len(deduped_issues['corrupted_json'])}</div>
                <div class="summary-item"><strong>Suspicious Empty Files:</strong> {len(deduped_issues['empty_files_suspicious'])}</div>
                <div class="summary-item"><strong>Broken Symbolic Links:</strong> {len(deduped_issues['broken_symlinks'])}</div>
                <div class="summary-item"><strong>TOTAL ISSUES:</strong> {total_issues}</div>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def send_email(self, subject, body_text, body_html):
        """Send email with both text and HTML versions"""
        if not all([self.config["sender_email"], self.config["recipient_email"]]):
            print("⚠️  Email configuration incomplete. Please set SENDER_EMAIL and RECIPIENT_EMAIL.")
            print("Example usage:")
            print("  export SENDER_EMAIL='your-email@example.com'")
            print("  export RECIPIENT_EMAIL='recipient@example.com'")
            print("  export SENDER_PASSWORD='your-app-password'")
            print("\nReport is available in tools/file_integrity_report.txt")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.config["sender_email"]
        msg['To'] = self.config["recipient_email"]
        
        # Attach both text and HTML versions
        part1 = MIMEText(body_text, 'plain')
        part2 = MIMEText(body_html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        try:
            if self.config["use_tls"]:
                server = smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"])
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.config["smtp_server"], self.config["smtp_port"])
            
            if self.config["sender_password"]:
                try:
                    server.login(self.config["sender_email"], self.config["sender_password"])
                except smtplib.SMTPAuthenticationError as auth_err:
                    print(f"❌ Authentication failed: {str(auth_err)}")
                    print("Please check your email and password (use App Password for Gmail)")
                    server.quit()
                    return False
            
            server.sendmail(
                self.config["sender_email"],
                self.config["recipient_email"],
                msg.as_string()
            )
            server.quit()
            
            print(f"✅ Email sent successfully to {self.config['recipient_email']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            print("\nPlease check your email configuration.")
            print("Report is available in tools/file_integrity_report.txt")
            return False


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Run integrity check
    print("Running file integrity check...")
    checker = FileIntegrityChecker(repo_root)
    checker.run_all_checks()
    
    # Generate text report
    text_report = checker.generate_report()
    print(text_report)
    
    # Save report to file
    report_file = os.path.join(repo_root, "tools", "file_integrity_report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(text_report)
    print(f"\n📄 Report saved to: {report_file}")
    
    # Send email
    reporter = EmailReporter()
    html_report = reporter.create_html_report(checker)
    
    total_issues = sum(len(v) for v in checker.get_issues_dict().values())
    subject = f"[W3_HB_team_BXCGICOG] File Integrity Report - {total_issues} Issue(s) Found" if total_issues > 0 else "[W3_HB_team_BXCGICOG] File Integrity Report - All Clear"
    
    reporter.send_email(subject, text_report, html_report)


if __name__ == "__main__":
    main()

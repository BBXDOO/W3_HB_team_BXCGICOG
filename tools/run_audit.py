#!/usr/bin/env python3
"""
W3 Security & Structural Audit - Master Orchestrator
Runs all audit agents in correct order

Execution Order:
1. DTML - Security Scanner (CRITICAL)
2. REDR - Structure Reader (HIGH)
3. PSP2 - PR Flow Router (MEDIUM)
4. LRC2 - System Recorder (ALWAYS-ON)
5. BBEX CORE - Philosophical Anchor (PASSIVE)
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


class AuditOrchestrator:
    def __init__(self):
        self.repo_path = Path(__file__).parent.parent
        self.tools_path = self.repo_path / 'tools'
        self.results = {}
        
    def print_header(self):
        """Print audit header"""
        print("=" * 70)
        print("W3 SECURITY & STRUCTURAL AUDIT")
        print("=" * 70)
        print()
        print(f"Repository: {self.repo_path.name}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Authority: BBX19 — Root Authority")
        print(f"Mode: RMB (Root-Model-Based)")
        print()
        print("=" * 70)
        print()
    
    def run_agent(self, name, script_name, priority):
        """Run an individual agent"""
        print(f"\n{'=' * 70}")
        print(f"AGENT: {name}")
        print(f"Priority: {priority}")
        print(f"{'=' * 70}\n")
        
        script_path = self.tools_path / script_name
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.repo_path,
                capture_output=False,
                text=True
            )
            
            self.results[name] = {
                'status': 'SUCCESS' if result.returncode == 0 else 'COMPLETED WITH WARNINGS',
                'exit_code': result.returncode
            }
            
            print()
            if result.returncode == 0:
                print(f"✅ {name} completed successfully")
            else:
                print(f"⚠️  {name} completed with warnings (exit code: {result.returncode})")
            
            return result.returncode
            
        except Exception as e:
            print(f"❌ Error running {name}: {str(e)}")
            self.results[name] = {
                'status': 'ERROR',
                'error': str(e)
            }
            return 1
    
    def print_summary(self):
        """Print execution summary"""
        print("\n" + "=" * 70)
        print("AUDIT SUMMARY")
        print("=" * 70 + "\n")
        
        print("Agent Execution Results:")
        print()
        for agent, result in self.results.items():
            status_icon = "✅" if result['status'] == 'SUCCESS' else "⚠️" if result['status'] == 'COMPLETED WITH WARNINGS' else "❌"
            print(f"{status_icon} {agent}: {result['status']}")
        
        print()
        print("=" * 70)
        print()
        print("Generated Reports:")
        print("  📄 DTML_Report.md - Security scan results")
        print("  📄 REDR_Structure_Map.md - Repository structure map")
        print("  📄 PR_Flow_Table.md - PR flow analysis")
        print("  📄 executions_log.json - System event log")
        print("  📄 decision_trace.md - Decision trace")
        print("  📄 BBEX_Reflection.md - Philosophical reflection")
        print()
        print("=" * 70)
        print()
        print("Next Steps:")
        print("  1. Review DTML_Report.md for security issues")
        print("  2. Verify REDR_Structure_Map.md for structural clarity")
        print("  3. Check PR_Flow_Table.md for merge guidance")
        print("  4. Review decision_trace.md for audit reasoning")
        print()
        print("=" * 70)
        print()
        print("Status: AUDIT COMPLETE")
        print("Authority: BBX19 — Root Authority")
        print("System: W3 Hybrid Team")
        print()
        print("=" * 70)
    
    def run_audit(self):
        """Execute complete audit"""
        self.print_header()
        
        # Agent 1: DTML (Security - CRITICAL)
        dtml_result = self.run_agent(
            "DTML (Detection Manual)",
            "dtml_security_scanner.py",
            "CRITICAL"
        )
        
        # Agent 2: REDR (Structure - HIGH)
        self.run_agent(
            "REDR (Reader)",
            "redr_structure_reader.py",
            "HIGH"
        )
        
        # Agent 3: PSP2 (PR Flow - MEDIUM)
        self.run_agent(
            "PSP2 (Pointer Stamp)",
            "psp2_pr_router.py",
            "MEDIUM"
        )
        
        # Agent 4: LRC2 (Logger - ALWAYS-ON)
        self.run_agent(
            "LRC2 (Log & Recorder)",
            "lrc2_recorder.py",
            "ALWAYS-ON"
        )
        
        # Agent 5: BBEX CORE (Philosophy - PASSIVE)
        self.run_agent(
            "BBEX CORE (Philosophical Anchor)",
            "bbex_core_anchor.py",
            "PASSIVE"
        )
        
        # Print summary
        self.print_summary()
        
        # Return exit code based on DTML result (security is critical)
        return dtml_result


def main():
    """Main execution"""
    orchestrator = AuditOrchestrator()
    exit_code = orchestrator.run_audit()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

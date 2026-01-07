# AGENT_TASKS.md
## Merge Review Requirements for W3 Hybrid System

---

## Purpose
This document defines the mandatory requirements that must be completed before any merge is approved in the W3 Hybrid repository. It ensures that all changes are properly documented, risks are assessed, and rollback procedures are in place.

---

## Merge Review Checklist

Before any merge request can be approved, the following sections must be completed:

### 1. Summary (สรุป)
A clear, concise summary of the changes must include:

- **What was changed?** — List all files, modules, and components modified
- **Why was it changed?** — Explain the motivation, issue being addressed, or feature being added
- **Who initiated?** — Identify the requesting module (human or AI)
- **Scope of impact** — List affected modules and dependencies
- **Expected outcome** — Describe the intended result after merge

**Format:**
```
[SUMMARY]
Changed: <list of changes>
Reason: <explanation>
Initiated by: <module/human name>
Affected modules: <module list>
Expected outcome: <description>
```

---

### 2. Risk Assessment (ประเมินความเสี่ยง)
Every change must be evaluated for potential risks:

- **Risk Level** — Rate as: LOW / MEDIUM / HIGH / CRITICAL
- **Impact Analysis** — What could break if this change fails?
- **Dependencies** — List any modules or systems that depend on this change
- **Breaking Changes** — Identify any backward-incompatible changes
- **Data Risk** — Assess potential for data loss or corruption
- **Security Risk** — Evaluate security implications

**Risk Classification:**
- **LOW:** Documentation updates, minor fixes with no logic changes
- **MEDIUM:** Feature additions, refactoring with tests
- **HIGH:** Core logic changes, governance updates, structural changes
- **CRITICAL:** Security fixes, data migrations, breaking changes

**Format:**
```
[RISK ASSESSMENT]
Risk Level: <LOW/MEDIUM/HIGH/CRITICAL>
Impact if failed: <description>
Dependencies: <list>
Breaking changes: <YES/NO - details>
Data risk: <description>
Security risk: <description>
Mitigation: <preventive measures>
```

---

### 3. Rollback Plan (แผนการย้อนกลับ)
A clear rollback procedure must be documented before merge:

- **Rollback Method** — How to undo the changes
- **Rollback Steps** — Step-by-step instructions
- **Rollback Time** — Estimated time to complete rollback
- **Data Preservation** — How to preserve data if rollback is needed
- **Verification** — How to verify successful rollback
- **Rollback Trigger** — Conditions that require rollback

**Format:**
```
[ROLLBACK PLAN]
Method: <git revert / manual / script>
Steps:
  1. <step 1>
  2. <step 2>
  3. <step 3>
Estimated time: <duration>
Data preservation: <procedure>
Verification: <how to verify>
Trigger conditions: <when to rollback>
```

---

## Review Requirements by Risk Level

### LOW Risk
- Summary: Required
- Risk Assessment: Required (brief)
- Rollback Plan: Required (can be simple git revert)
- Reviewers: 1 AI module

### MEDIUM Risk
- Summary: Required (detailed)
- Risk Assessment: Required (complete)
- Rollback Plan: Required (detailed steps)
- Reviewers: 1 AI module + peer review

### HIGH Risk
- Summary: Required (comprehensive)
- Risk Assessment: Required (complete with mitigation)
- Rollback Plan: Required (tested procedure)
- Reviewers: Gemini validation + 1 AI module
- Testing: Required before merge

### CRITICAL Risk
- Summary: Required (comprehensive)
- Risk Assessment: Required (complete with mitigation)
- Rollback Plan: Required (tested and documented)
- Reviewers: Gemini + BBX19 approval
- Testing: Required with backup verification
- Escalation: Document in `/Grok/insight-vault/incidents.md` if issues arise

---

## Compliance with W3 Governance

All merge reviews must align with:

1. **Operating Guidelines** — See `core/governance/operating-guidelines.md`
2. **No direct commit to main**
3. **PR must be reviewed by at least 1 AI engine**
4. **Gemini required for high-risk docs**
5. **BBX19 exclusive override** for critical decisions

---

## Failure Handling Protocol

If any required section is incomplete:

1. **HOLD MERGE** — Do not proceed with merge
2. **Request Completion** — Ask the initiating module to complete missing sections
3. **Document Blocker** — Note which sections are incomplete
4. **Escalate if needed** — If unclear, escalate to Gemini or Copilot-Gm

**Example Response:**
```
ขอ hold merge ไว้ก่อนครับ ขอ review summary + risk + rollback ให้ครบก่อน ตาม AGENT_TASKS.md

Missing:
- [ ] Summary
- [ ] Risk Assessment
- [ ] Rollback Plan
```

---

## Template for Merge Review

Use this template in PR description or comment:

```markdown
## 📋 Merge Review — AGENT_TASKS Compliance

### [SUMMARY]
Changed: 
Reason: 
Initiated by: 
Affected modules: 
Expected outcome: 

### [RISK ASSESSMENT]
Risk Level: 
Impact if failed: 
Dependencies: 
Breaking changes: 
Data risk: 
Security risk: 
Mitigation: 

### [ROLLBACK PLAN]
Method: 
Steps:
  1. 
  2. 
  3. 
Estimated time: 
Data preservation: 
Verification: 
Trigger conditions: 

---
Reviewed by: 
Date: 
Approval status: 
```

---

## Integration with Existing Protocols

This document complements:

- **Pull Request Template** — `.github/PULL_REQUEST_TEMPLATE.md`
- **Incident Vault** — `Grok/insight-vault/ncidents.md`
- **Live Prototype Protocol** — `ChatGPT/prototypes/live.md`
- **Audit Checklist** — `docs/audit-checklist.md`
- **Governance Principles** — `governance` (root file)

---

## Principles

**P1** — Transparency over speed  
**P2** — Every change is reversible  
**P3** — No merge without accountability  
**P4** — Understanding leads principles

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-16  
**Owner:** W3 Hybrid System  
**Signed by:** Copilot-Gm (Governance Engine)

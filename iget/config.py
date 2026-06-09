# ==========================================
# IGET v6.0 — Configuration
# ==========================================

VERSION = "6.0"

# ── Output limits ──────────────────────────────────────────────
MAX_INLINE_COMMENTS = 5

# ── File classification ────────────────────────────────────────
CODE_EXT = (
    ".py", ".js", ".ts", ".tsx",
    ".jsx", ".json", ".yml", ".yaml",
    ".css", ".html", ".go", ".java",
    ".rb", ".php", ".c", ".cpp", ".h",
    ".sh", ".rs", ".swift", ".kt",
)

DOC_EXT = (".md", ".txt", ".rst", ".adoc")

CONFIG_EXT = (
    ".yml", ".yaml", ".json", ".toml",
    ".ini", ".cfg", ".env", ".conf",
)

RISK_WORDS = [
    ".env", "secret", "token", "password",
    "credential", "private_key", "apikey",
    "api_key", "auth_key", "access_key",
    "client_secret",
]

SCORE_GREEN = 85
SCORE_YELLOW = 60
FILES_WARN = 6
FILES_LARGE = 15
CHANGES_WARN = 400
CHANGES_LARGE = 800
GITHUB_PAGE_SIZE = 100

# ── v8.0 — Semantic State Definitions ─────────────────────────
# Ontology tag: iget:semantic_state
SEMANTIC_STATES = {
    "safe":      "PR พร้อม merge ไม่มีความเสี่ยงสำคัญ",
    "caution":   "PR มีจุดที่ควรตรวจสอบก่อน merge",
    "critical":  "PR มีความเสี่ยงสูง ต้องการ review เชิงลึก",
    "unknown":   "ไม่สามารถประเมิน semantic state ได้",
}

# ── v8.0 — MPCP Claim Tags ─────────────────────────────────────
# Ontology tag: iget:mpcp_role = "governance_assistant"
MPCP_ROLE     = "governance_assistant"
MPCP_VERSION  = "1.0"

# ── v8.0 — Recovery / Resilience ──────────────────────────────
MAX_FETCH_RETRY    = 3
CHECKPOINT_ENABLED = True
ROLLBACK_ON_FAIL   = True

# ── v8.0 — Proof Trace Settings ───────────────────────────────
PROOF_TRACE_ENABLED = True
PROOF_MAX_ENTRIES   = 50

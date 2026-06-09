"""IGET v9 runtime and scoring configuration."""

from __future__ import annotations

VERSION = "9.0"
COMMENT_MARKER = "<!-- iget:summary -->"
DEFAULT_API_URL = "https://api.github.com"
DEFAULT_TIMEOUT = 20.0
MAX_INLINE_COMMENTS = 5

CODE_EXT = (
    ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yml", ".yaml",
    ".css", ".html", ".go", ".java", ".rb", ".php", ".c", ".cpp",
    ".h", ".sh", ".rs", ".swift", ".kt",
)
DOC_EXT = (".md", ".txt", ".rst", ".adoc")
CONFIG_EXT = (".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".env", ".conf")
RISK_WORDS = [
    ".env", "secret", "token", "password", "credential", "private_key",
    "apikey", "api_key", "auth_key", "access_key", "client_secret",
]

SCORE_GREEN = 85
SCORE_YELLOW = 60
FILES_WARN = 6
FILES_LARGE = 15
CHANGES_WARN = 400
CHANGES_LARGE = 800
GITHUB_PAGE_SIZE = 100

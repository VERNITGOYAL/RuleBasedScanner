from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent

# Output folders
OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = OUTPUT_DIR / "reports"
DATABASE_DIR = OUTPUT_DIR / "database"

# Logs
LOG_DIR = BASE_DIR / "logs"

# Scanner configuration
MAX_CRAWL_DEPTH = 2
REQUEST_TIMEOUT = 10

USER_AGENT = (
    "RuleBasedScanner/1.0 "
    "(Educational Project - Authorized Testing Only)"
)
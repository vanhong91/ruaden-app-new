### dùng bcrypt và PostgreSQL 

import os
import logging
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("config")

# ------------------------------------------------------------------------------
# Database configuration
# ------------------------------------------------------------------------------
DB_TYPE = os.getenv("DB_TYPE", "postgres").strip().lower()

# Hỗ trợ cả postgres và postgresql
if DB_TYPE in ("postgres", "postgresql"):
    DB_URL = os.getenv("DB_URL", "").strip()
    if not DB_URL:
        raise ValueError(
            "❌ DB_URL is not set in .env file. Please define it for PostgreSQL connection.\n"
            "Example:\n"
            "    DB_TYPE=postgres\n"
            "    DB_URL=postgresql://user:password@localhost:5432/dbname"
        )
    logger.info("✅ Using PostgreSQL database at %s", DB_URL)
elif DB_TYPE == "sqlite":
    DB_URL = os.getenv("SQLITE_DB_PATH", os.path.abspath("data.db")).strip()
    if not DB_URL:
        DB_URL = os.path.abspath("data.db")
    logger.warning("⚠️ Falling back to SQLite database at %s", DB_URL)
else:
    raise ValueError(
        f"❌ Unsupported DB_TYPE '{DB_TYPE}'. Use one of: 'postgres', 'postgresql', or 'sqlite'."
    )

# ------------------------------------------------------------------------------
# Application configuration
# ------------------------------------------------------------------------------
APP_TITLE_EN = "What to Cook Today"
APP_TITLE_VI = "Hôm Nay Nấu Gì"

# ------------------------------------------------------------------------------
# Debug info (safe, only prints last part of URL for security)
# ------------------------------------------------------------------------------
if logger.isEnabledFor(logging.DEBUG):
    safe_url = DB_URL
    if "@" in DB_URL:
        # Ẩn mật khẩu trong URL
        parts = DB_URL.split("@")
        left = parts[0].split("//")
        if len(left) == 2:
            safe_url = f"{left[0]}//***:***@{parts[1]}"
    logger.debug("DB_TYPE=%s", DB_TYPE)
    logger.debug("DB_URL=%s", safe_url)

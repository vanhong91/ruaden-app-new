import sqlite3
import bcrypt
import logging

# Cấu hình logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def migrate_passwords(db_name: str):
    """Migrate plaintext passwords to bcrypt hashes in SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        cur.execute("SELECT id, username, password FROM users")
        users = cur.fetchall()

        for user in users:
            user_id = user["id"]
            username = user["username"]
            password = user["password"]

            # Nếu password là bytes -> decode
            if isinstance(password, bytes):
                password = password.decode("utf-8")

            # Kiểm tra nếu mật khẩu chưa được mã hóa bằng bcrypt
            if not str(password).startswith("$2b$"):
                logger.info(f"Migrating password for user: {username}")
                hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                cur.execute(
                    "UPDATE users SET password = ? WHERE id = ?",
                    (hashed.decode("utf-8"), user_id)
                )

        conn.commit()
        logger.info("✅ Password migration completed successfully.")

    except sqlite3.Error as e:
        logger.error(f"❌ Error during migration: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_passwords("data.db")  # Thay bằng tên DB nếu khác

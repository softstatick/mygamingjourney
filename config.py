import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

try:
    from dotenv import load_dotenv

    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass


def _get_secret_key():
    key = os.environ.get("SECRET_KEY")
    if not key:
        raise RuntimeError(
            "SECRET_KEY tidak di-set. Tambahkan SECRET_KEY ke environment atau file .env."
        )
    return key


def _get_database_uri():
    # Override langsung via DATABASE_URL, atau pakai variabel terpisah di bawah
    if os.environ.get("DATABASE_URL"):
        return os.environ["DATABASE_URL"]
    user = os.environ.get("DB_USER", "root")
    password = os.environ.get("DB_PASSWORD", "")
    host = os.environ.get("DB_HOST", "localhost")
    name = os.environ.get("DB_NAME", "mygamingjourney")
    return f"mysql+pymysql://{user}:{password}@{host}/{name}"


class Config:
    # Session
    SECRET_KEY = _get_secret_key()

    # Debug / port bisa di-set via FLASK_DEBUG dan FLASK_PORT
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
    PORT = int(os.environ.get("FLASK_PORT", 5000))

    # Database (default MySQL; lihat _get_database_uri untuk override)
    SQLALCHEMY_DATABASE_URI = _get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Folder upload foto profil
    UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Max 5 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def allowed_file(filename):
    """Cek apakah ekstensi file diizinkan."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

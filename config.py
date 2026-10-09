import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ganti-ini-dengan-random-string-panjang")
    
    # Database SQLite di folder project
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'mygamingjourney.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Folder upload foto profil
    UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Max 5 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
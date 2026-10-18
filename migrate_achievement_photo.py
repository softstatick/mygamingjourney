import sqlite3
from pathlib import Path

# Karena udah pindah ke MySQL, kita gak butuh sqlite3.
# Kita pake script python buat ngejalanin query ALTER TABLE via SQLAlchemy.

from app import create_app
from models.models import db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        try:
            # Cek apakah kolom 'foto' udah ada di tabel achievements
            result = db.session.execute(text("SHOW COLUMNS FROM achievements LIKE 'foto'")).fetchone()
            
            if not result:
                print("  → Menambahkan kolom 'foto' ke tabel achievements...")
                db.session.execute(text("ALTER TABLE achievements ADD COLUMN foto VARCHAR(255) NULL"))
                db.session.commit()
                print("  ✅ Kolom 'foto' berhasil ditambahkan.")
            else:
                print("  ⏭️  Kolom 'foto' sudah ada. Skip.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate()
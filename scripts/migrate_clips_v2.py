"""
Migration v2 — tambah kolom deskripsi di tabel clips.
Jalanin SEKALI aja: python migrate_clips_v2.py
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "mygamingjourney.db"


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return column in [row[1] for row in cursor.fetchall()]


def migrate():
    if not DB_PATH.exists():
        print("❌ Database belum ada!")
        return
    
    print(f"📂 Database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if not column_exists(cursor, "clips", "deskripsi"):
        print("  → Tambah kolom clips.deskripsi")
        cursor.execute("ALTER TABLE clips ADD COLUMN deskripsi TEXT")
        print("  ✅ Kolom deskripsi dibuat")
    else:
        print("  ⏭️  Kolom deskripsi udah ada")
    
    conn.commit()
    conn.close()
    print("\n🎉 Migration SUKSES!")


if __name__ == "__main__":
    migrate()
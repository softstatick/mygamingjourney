"""
Script migration database.
Jalanin SEKALI aja: python migrate_db.py

Kegunaan: 
- Rename game_role → game_role_1 (kalau belum)
- Tambah game_role_2, game_role_3, is_all_role
- Rename kda → mvp
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
        print("❌ Database belum ada. Jalanin `python app.py` dulu.")
        return
    
    print(f"📂 Database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    changes = 0
    
    # === ROLE MIGRATION ===
    if column_exists(cursor, "profiles", "game_role") and not column_exists(cursor, "profiles", "game_role_1"):
        print("  → Rename game_role → game_role_1")
        try:
            cursor.execute("ALTER TABLE profiles RENAME COLUMN game_role TO game_role_1")
            changes += 1
        except:
            pass
    
    for col in ["game_role_1", "game_role_2", "game_role_3"]:
        if not column_exists(cursor, "profiles", col):
            print(f"  → Tambah kolom {col}")
            cursor.execute(f"ALTER TABLE profiles ADD COLUMN {col} VARCHAR(30)")
            changes += 1
    
    if not column_exists(cursor, "profiles", "is_all_role"):
        print("  → Tambah kolom is_all_role")
        cursor.execute("ALTER TABLE profiles ADD COLUMN is_all_role BOOLEAN DEFAULT 0")
        changes += 1
    
    # === KDA → MVP MIGRATION ===
    if column_exists(cursor, "profiles", "kda") and not column_exists(cursor, "profiles", "mvp"):
        print("  → Rename kda → mvp")
        try:
            cursor.execute("ALTER TABLE profiles RENAME COLUMN kda TO mvp")
            changes += 1
        except:
            # Fallback: bikin mvp baru, copy data dari kda
            cursor.execute("ALTER TABLE profiles ADD COLUMN mvp INTEGER DEFAULT 0")
            cursor.execute("UPDATE profiles SET mvp = CAST(kda AS INTEGER)")
            changes += 1
    elif not column_exists(cursor, "profiles", "mvp"):
        print("  → Tambah kolom mvp")
        cursor.execute("ALTER TABLE profiles ADD COLUMN mvp INTEGER DEFAULT 0")
        changes += 1
    
    conn.commit()
    conn.close()
    
    if changes == 0:
        print("\n⏭️  Database udah up-to-date. Skip.")
    else:
        print(f"\n🎉 Migration SUKSES! {changes} perubahan.")


if __name__ == "__main__":
    migrate()
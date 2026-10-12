"""
Script migration database.
Jalanin SEKALI aja: python migrate_db.py

Kegunaan: Update struktur tabel profiles biar support multi-role.
- Rename game_role → game_role_1
- Tambah game_role_2, game_role_3, is_all_role
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "mygamingjourney.db"


def check_column_exists(cursor, table, column):
    """Cek apakah kolom udah ada di tabel."""
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    return column in columns


def migrate():
    if not DB_PATH.exists():
        print("❌ Database belum ada. Jalanin `python app.py` dulu.")
        return
    
    print(f"📂 Database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cek kolom lama `game_role` ada atau nggak
    has_old = check_column_exists(cursor, "profiles", "game_role")
    has_new = check_column_exists(cursor, "profiles", "game_role_1")
    
    if has_new:
        print("⏭️  Kolom game_role_1 udah ada. Skip migration.")
        conn.close()
        return
    
    print("\n🔧 Mulai migration...")
    
    if has_old:
        print("  → Rename game_role → game_role_1")
        try:
            cursor.execute("ALTER TABLE profiles RENAME COLUMN game_role TO game_role_1")
            print("  ✅ Rename berhasil")
        except sqlite3.OperationalError as e:
            print(f"  ⚠️  Rename gagal: {e}")
            print("  → Coba cara lain: bikin kolom baru")
            cursor.execute("ALTER TABLE profiles ADD COLUMN game_role_1 VARCHAR(30) DEFAULT 'Jungler'")
            cursor.execute("UPDATE profiles SET game_role_1 = game_role")
            print("  ✅ Kolom game_role_1 dibuat + data dicopy")
    else:
        print("  → Kolom game_role gak ada. Bikin game_role_1 baru")
        cursor.execute("ALTER TABLE profiles ADD COLUMN game_role_1 VARCHAR(30) DEFAULT 'Jungler'")
        print("  ✅ Kolom game_role_1 dibuat")
    
    # Tambah kolom baru
    if not check_column_exists(cursor, "profiles", "game_role_2"):
        print("  → Tambah kolom game_role_2")
        cursor.execute("ALTER TABLE profiles ADD COLUMN game_role_2 VARCHAR(30)")
        print("  ✅ Kolom game_role_2 dibuat")
    
    if not check_column_exists(cursor, "profiles", "game_role_3"):
        print("  → Tambah kolom game_role_3")
        cursor.execute("ALTER TABLE profiles ADD COLUMN game_role_3 VARCHAR(30)")
        print("  ✅ Kolom game_role_3 dibuat")
    
    if not check_column_exists(cursor, "profiles", "is_all_role"):
        print("  → Tambah kolom is_all_role")
        cursor.execute("ALTER TABLE profiles ADD COLUMN is_all_role BOOLEAN DEFAULT 0")
        print("  ✅ Kolom is_all_role dibuat")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Migration SUKSES!")
    print("📊 Data lama aman, kolom baru siap dipakai.")


if __name__ == "__main__":
    migrate()
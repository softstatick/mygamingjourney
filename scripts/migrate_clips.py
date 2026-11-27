"""
Script migration untuk tabel clips (Fase 4B-3a).
Jalanin SEKALI aja: python migrate_clips.py

Yang dilakuin:
- Tambah kolom platform, video_id, thumbnail, upvotes, downvotes, report_count, is_hidden
- Hapus kolom link lama kalau ada? (kita tetep keep link asli)
- Bikin tabel votes baru
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "mygamingjourney.db"


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return column in [row[1] for row in cursor.fetchall()]


def table_exists(cursor, table):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cursor.fetchone() is not None


def migrate():
    if not DB_PATH.exists():
        print("❌ Database belum ada. Jalanin `python app.py` dulu.")
        return
    
    print(f"📂 Database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # === Tabel clips ===
    if not table_exists(cursor, "clips"):
        print("⚠️  Tabel clips gak ada. Bikin tabel baru...")
        cursor.execute("""
            CREATE TABLE clips (
                id INTEGER PRIMARY KEY,
                profile_id INTEGER NOT NULL,
                judul VARCHAR(150) NOT NULL,
                link VARCHAR(500) NOT NULL,
                platform VARCHAR(20) NOT NULL,
                video_id VARCHAR(100) NOT NULL,
                thumbnail VARCHAR(500),
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                report_count INTEGER DEFAULT 0,
                is_hidden BOOLEAN DEFAULT 0,
                created_at DATETIME,
                FOREIGN KEY (profile_id) REFERENCES profiles(id)
            )
        """)
        print("  ✅ Tabel clips dibuat")
    else:
        # Tambah kolom baru satu-satu
        new_columns = [
            ("platform", "VARCHAR(20)"),
            ("video_id", "VARCHAR(100)"),
            ("thumbnail", "VARCHAR(500)"),
            ("upvotes", "INTEGER DEFAULT 0"),
            ("downvotes", "INTEGER DEFAULT 0"),
            ("report_count", "INTEGER DEFAULT 0"),
            ("is_hidden", "BOOLEAN DEFAULT 0"),
        ]
        for col_name, col_type in new_columns:
            if not column_exists(cursor, "clips", col_name):
                print(f"  → Tambah kolom clips.{col_name}")
                cursor.execute(f"ALTER TABLE clips ADD COLUMN {col_name} {col_type}")
        
        # Hapus kolom created_at lama kalau belum ada (kitanya keep)
        if not column_exists(cursor, "clips", "created_at"):
            cursor.execute("ALTER TABLE clips ADD COLUMN created_at DATETIME")
    
    # === Tabel votes ===
    if not table_exists(cursor, "votes"):
        print("  → Bikin tabel votes")
        cursor.execute("""
            CREATE TABLE votes (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                clip_id INTEGER NOT NULL,
                vote_type INTEGER NOT NULL,
                created_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (clip_id) REFERENCES clips(id),
                UNIQUE(user_id, clip_id)
            )
        """)
        print("  ✅ Tabel votes dibuat")
    else:
        print("  ⏭️  Tabel votes udah ada")
    
    # === Tabel achievements — tambah created_at kalau belum ada ===
    if table_exists(cursor, "achievements"):
        if not column_exists(cursor, "achievements", "created_at"):
            print("  → Tambah kolom achievements.created_at")
            cursor.execute("ALTER TABLE achievements ADD COLUMN created_at DATETIME")
    else:
        print("  → Bikin tabel achievements")
        cursor.execute("""
            CREATE TABLE achievements (
                id INTEGER PRIMARY KEY,
                profile_id INTEGER NOT NULL,
                judul VARCHAR(150) NOT NULL,
                deskripsi TEXT,
                tanggal DATE,
                created_at DATETIME,
                FOREIGN KEY (profile_id) REFERENCES profiles(id)
            )
        """)
        print("  ✅ Tabel achievements dibuat")
    
    conn.commit()
    conn.close()
    print("\n🎉 Migration SUKSES!")


if __name__ == "__main__":
    migrate()
"""
Script fix tipe kolom mvp dari FLOAT ke INTEGER.
Jalanin SEKALI aja: python fix_mvp_type.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "mygamingjourney.db"


def fix_mvp_type():
    if not DB_PATH.exists():
        print("❌ Database gak ada!")
        return
    
    print(f"📂 Database: {DB_PATH}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cek tipe kolom mvp sekarang
    cursor.execute("PRAGMA table_info(profiles)")
    cols = cursor.fetchall()
    
    mvp_col = None
    for col in cols:
        if col[1] == "mvp":
            mvp_col = col
            break
    
    if not mvp_col:
        print("❌ Kolom mvp gak ada!")
        conn.close()
        return
    
    current_type = mvp_col[2]
    print(f"📊 Tipe kolom mvp sekarang: {current_type}")
    
    if current_type == "INTEGER":
        print("✅ Kolom mvp udah INTEGER. Skip.")
        conn.close()
        return
    
    print("\n🔧 Mulai fix...")
    
    # Ambil semua data profile
    cursor.execute("SELECT * FROM profiles")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    
    # Bikin tabel baru dengan skema yang bener
    print("  → Bikin tabel profiles_new")
    cursor.execute("""
        CREATE TABLE profiles_new (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL,
            nama_lengkap VARCHAR(100),
            nickname VARCHAR(50),
            foto VARCHAR(255),
            bio TEXT,
            rank VARCHAR(30) DEFAULT 'Mythic',
            game_role_1 VARCHAR(30) DEFAULT 'Jungler',
            game_role_2 VARCHAR(30),
            game_role_3 VARCHAR(30),
            is_all_role BOOLEAN DEFAULT 0,
            region VARCHAR(50) DEFAULT 'Indonesia',
            winrate FLOAT DEFAULT 0.0,
            total_match INTEGER DEFAULT 0,
            mvp INTEGER DEFAULT 0,
            availability VARCHAR(20) DEFAULT 'open',
            kontak_wa VARCHAR(30),
            kontak_discord VARCHAR(50),
            kontak_ig VARCHAR(50),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    
    # Copy data dari tabel lama ke baru
    print("  → Copy data ke tabel baru")
    mvp_idx = columns.index("mvp") if "mvp" in columns else None
    
    for row in rows:
        row = list(row)
        # Konversi mvp ke integer kalau ada
        if mvp_idx is not None and row[mvp_idx] is not None:
            try:
                row[mvp_idx] = int(row[mvp_idx])
            except:
                row[mvp_idx] = 0
        
        placeholders = ",".join(["?"] * len(row))
        cursor.execute(f"INSERT INTO profiles_new VALUES ({placeholders})", row)
    
    # Drop tabel lama, rename tabel baru
    print("  → Hapus tabel profiles lama")
    cursor.execute("DROP TABLE profiles")
    
    print("  → Rename profiles_new → profiles")
    cursor.execute("ALTER TABLE profiles_new RENAME TO profiles")
    
    conn.commit()
    
    # Verifikasi
    cursor.execute("PRAGMA table_info(profiles)")
    mvp_col_new = [c for c in cursor.fetchall() if c[1] == "mvp"][0]
    print(f"\n📊 Tipe kolom mvp baru: {mvp_col_new[2]}")
    
    conn.close()
    
    print("\n🎉 FIX SUKSES!")


if __name__ == "__main__":
    fix_mvp_type()
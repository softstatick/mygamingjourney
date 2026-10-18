"""
Script buat mindahin data dari SQLite ke MySQL (XAMPP).
Jalanin SEKALI aja: python migrate_to_mysql.py
"""
import sqlite3
from app import create_app
from models.models import db, User, Profile, HeroMaster, Hero, Clip, Achievement

SQLITE_DB_PATH = "mygamingjourney.db"

def migrate():
    print("🚀 Memulai migrasi data dari SQLite ke MySQL...")
    
    # Koneksi ke SQLite
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Bikin tabel di MySQL (via SQLAlchemy)
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Tabel MySQL berhasil dibuat.")
        
        # Hapus data lama di MySQL (kalau ada, biar gak dobel)
        Hero.query.delete()
        Clip.query.delete()
        Achievement.query.delete()
        Profile.query.delete()
        User.query.delete()
        HeroMaster.query.delete()
        db.session.commit()
        print("🗑️ Data MySQL lama dibersihkan.")
        
        # 1. Migrasi HeroMaster
        print("Migrasi HeroMaster...")
        cursor.execute("SELECT * FROM heroes_master")
        for row in cursor.fetchall():
            db.session.add(HeroMaster(id=row['id'], name=row['name'], image_url=row['image_url'], role=row['role']))
        
        # 2. Migrasi Users
        print("Migrasi Users...")
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            db.session.add(User(id=row['id'], username=row['username'], email=row['email'], password=row['password'], role=row['role']))
            
        # 3. Migrasi Profiles
        print("Migrasi Profiles...")
        cursor.execute("SELECT * FROM profiles")
        for row in cursor.fetchall():
            db.session.add(Profile(
                id=row['id'], user_id=row['user_id'], nama_lengkap=row['nama_lengkap'], nickname=row['nickname'],
                bio=row['bio'], rank=row['rank'], game_role_1=row['game_role_1'], game_role_2=row['game_role_2'],
                game_role_3=row['game_role_3'], is_all_role=bool(row['is_all_role']), region=row['region'],
                winrate=row['winrate'], total_match=row['total_match'], mvp=row['mvp'], availability=row['availability'],
                kontak_wa=row['kontak_wa'], kontak_discord=row['kontak_discord'], kontak_ig=row['kontak_ig']
            ))
            
        db.session.commit() # Commit dulu sebelum tabel relasi
        
        # 4. Migrasi Heroes
        print("Migrasi Heroes...")
        cursor.execute("SELECT * FROM heroes")
        for row in cursor.fetchall():
            db.session.add(Hero(id=row['id'], profile_id=row['profile_id'], master_hero_id=row['master_hero_id'], winrate=row['winrate'], total_match=row['total_match']))
            
        # 5. Migrasi Clips
        print("Migrasi Clips...")
        cursor.execute("SELECT * FROM clips")
        for row in cursor.fetchall():
            db.session.add(Clip(
                id=row['id'], profile_id=row['profile_id'], judul=row['judul'], link=row['link'], 
                platform=row['platform'], video_id=row['video_id'], thumbnail=row['thumbnail'],
                upvotes=row['upvotes'], downvotes=row['downvotes'], deskripsi=row['deskripsi']
            ))
            
        # 6. Migrasi Achievements
        print("Migrasi Achievements...")
        cursor.execute("SELECT * FROM achievements")
        for row in cursor.fetchall():
            db.session.add(Achievement(id=row['id'], profile_id=row['profile_id'], judul=row['judul'], deskripsi=row['deskripsi'], tanggal=row['tanggal']))
            
        db.session.commit()
        print("🎉 MIGRASI SELESAI! Data lo udah pindah ke MySQL.")
        
    conn.close()

if __name__ == "__main__":
    migrate()
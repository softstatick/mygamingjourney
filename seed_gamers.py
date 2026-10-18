"""
Script untuk nambahin 5 gamer dummy ke database.
Jalanin SEKALI aja: python seed_gamers.py
"""

from app import create_app
from models.models import db, User, Profile
from werkzeug.security import generate_password_hash

# Data 5 Gamer Dummy (ML)
DUMMY_GAMERS = [
    {
        "username": "raven.id",
        "email": "raven@demo.com",
        "nickname": "Raven",
        "nama_lengkap": "Raven Pratama",
        "bio": "Main assassin dengan tempo tinggi dan objektif rapi. Spesialis early game pressure.",
        "rank": "Mythical Glory",
        "game_role_1": "Jungler",
        "region": "Jakarta",
        "winrate": 68.4,
        "total_match": 1280,
        "mvp": 340,
        "availability": "open",
    },
    {
        "username": "mikael",
        "email": "mikael@demo.com",
        "nickname": "Mikael",
        "nama_lengkap": "Mikael Santoso",
        "bio": "Mage player yang kuat di teamfight dan rotasi. Paham meta terkini.",
        "rank": "Mythic",
        "game_role_1": "Mid",
        "region": "Bandung",
        "winrate": 64.8,
        "total_match": 942,
        "mvp": 210,
        "availability": "open",
    },
    {
        "username": "nox.esp",
        "email": "nox@demo.com",
        "nickname": "Nox",
        "nama_lengkap": "Nox Wijaya",
        "bio": "Roamer komunikatif, vision selalu aktif. Specialist setup kill.",
        "rank": "Mythical Honor",
        "game_role_1": "Roam",
        "region": "Surabaya",
        "winrate": 62.1,
        "total_match": 1104,
        "mvp": 180,
        "availability": "open",
    },
    {
        "username": "aluna.ml",
        "email": "aluna@demo.com",
        "nickname": "Aluna",
        "nama_lengkap": "Aluna Putri",
        "bio": "Gold lane presisi dengan farming disiplin. Positioning selalu aman.",
        "rank": "Mythic",
        "game_role_1": "Gold",
        "region": "Yogyakarta",
        "winrate": 60.7,
        "total_match": 786,
        "mvp": 150,
        "availability": "closed",
    },
    {
        "username": "bima.exp",
        "email": "bima.exp@demo.com",
        "nickname": "Bima",
        "nama_lengkap": "Bima Aditya",
        "bio": "Exp laner tahan tekanan dan berani membuka map. Split push specialist.",
        "rank": "Mythical Glory",
        "game_role_1": "Exp",
        "region": "Medan",
        "winrate": 66.2,
        "total_match": 1350,
        "mvp": 280,
        "availability": "open",
    },
]


def seed():
    app = create_app()
    with app.app_context():
        print("🌱 Mulai nambahin gamer dummy...")
        
        created = 0
        skipped = 0
        
        for data in DUMMY_GAMERS:
            # Cek kalau username udah ada
            existing = User.query.filter_by(username=data["username"]).first()
            if existing:
                print(f"⏭️  Skip {data['nickname']} (udah ada)")
                skipped += 1
                continue
            
            # Bikin User
            user = User(
                username=data["username"],
                email=data["email"],
                password=generate_password_hash("demo123"), # Password default
                role="gamer"
            )
            db.session.add(user)
            db.session.flush() # Biar dapet user.id
            
            # Bikin Profile
            profile = Profile(
                user_id=user.id,
                nickname=data["nickname"],
                nama_lengkap=data["nama_lengkap"],
                bio=data["bio"],
                rank=data["rank"],
                game_role_1=data["game_role_1"],
                region=data["region"],
                winrate=data["winrate"],
                total_match=data["total_match"],
                mvp=data["mvp"],
                availability=data["availability"]
            )
            db.session.add(profile)
            created += 1
            print(f"✅ {data['nickname']} (@{data['username']})")
        
        db.session.commit()
        print(f"\n🎉 Selesai! Dibuat: {created}, Di-skip: {skipped}")


if __name__ == "__main__":
    seed()
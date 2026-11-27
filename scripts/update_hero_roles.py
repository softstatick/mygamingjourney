"""
Script update role untuk 133 hero ML.
Jalanin SEKALI aja: python update_hero_roles.py

Format role: CSV string (contoh: "Mage,Assassin")
Kalau hero punya 1 role: "Fighter"
Kalau hero punya 2 role: "Assassin,Fighter"
"""

from app import create_app
from models.models import db, HeroMaster


# Mapping 133 hero ML → role(s)
# Kalau multi-role, tulis dengan koma: "Assassin,Fighter"
HERO_ROLES = {
    # === ASSASSIN ===
    "Saber": "Assassin",
    "Karina": "Assassin,Mage",
    "Fanny": "Assassin",
    "Hayabusa": "Assassin",
    "Natalia": "Assassin",
    "Lancelot": "Assassin",
    "Gusion": "Assassin,Mage",
    "Helcurt": "Assassin",
    "Lesley": "Assassin,Marksman",
    "Hanzo": "Assassin",
    "Harley": "Assassin,Mage",
    "Selena": "Assassin,Mage",
    "Benedetta": "Assassin",
    "Aamon": "Assassin",
    "Joy": "Assassin",
    "Nolan": "Assassin",
    "Hirara": "Assassin",
    "Ling": "Assassin",
    "Yi Sun-shin": "Assassin,Fighter",
    "Yin": "Assassin,Fighter",
    
    # === FIGHTER ===
    "Balmond": "Fighter,Tank",
    "Alucard": "Fighter,Assassin",
    "Bane": "Fighter,Mage",
    "Zilong": "Fighter,Assassin",
    "Freya": "Fighter",
    "Chou": "Fighter,Assassin",
    "Sun": "Fighter",
    "Alpha": "Fighter",
    "Ruby": "Fighter,Tank",
    "Jawhead": "Fighter",
    "Hilda": "Fighter,Tank",
    "Lapu-Lapu": "Fighter",
    "Argus": "Fighter,Assassin",
    "Martis": "Fighter",
    "Aldous": "Fighter",
    "Guinevere": "Fighter,Mage",
    "Terizla": "Fighter",
    "X.Borg": "Fighter",
    "Dyrroth": "Fighter,Assassin",
    "Masha": "Fighter,Tank",
    "Silvanna": "Fighter,Mage",
    "Yu Zhong": "Fighter",
    "Khaleed": "Fighter",
    "Paquito": "Fighter",
    "Phoveus": "Fighter",
    "Aulus": "Fighter",
    "Julian": "Fighter,Assassin",
    "Fredrinn": "Fighter,Tank",
    "Arlott": "Fighter,Assassin",
    "Cici": "Fighter,Marksman",
    "Suyou": "Fighter,Assassin",
    "Lukas": "Fighter",
    "Sora": "Fighter,Tank",
    "Leomord": "Fighter",
    "Minsitthar": "Fighter,Roam",
    "Badang": "Fighter",
    "Thamuz": "Fighter",
    
    # === MAGE ===
    "Alice": "Mage,Tank",
    "Nana": "Mage",
    "Eudora": "Mage",
    "Gord": "Mage",
    "Kagura": "Mage",
    "Aurora": "Mage",
    "Vexana": "Mage",
    "Odette": "Mage",
    "Valir": "Mage",
    "Chang'e": "Mage",
    "Vale": "Mage",
    "Lylia": "Mage",
    "Cecilion": "Mage",
    "Luo Yi": "Mage",
    "Yve": "Mage",
    "Valentina": "Mage",
    "Xavier": "Mage",
    "Novaria": "Mage",
    "Zetian": "Mage",
    "Zhask": "Mage",
    "Cyclops": "Mage",
    "Pharsa": "Mage",
    "Harith": "Mage,Assassin",
    "Kadita": "Mage,Assassin",
    "Lunox": "Mage",
    "Esmeralda": "Mage,Tank",
    "Zhuxin": "Mage",
    
    # === MARKSMAN ===
    "Miya": "Marksman",
    "Bruno": "Marksman",
    "Clint": "Marksman",
    "Layla": "Marksman",
    "Moskov": "Marksman",
    "Karrie": "Marksman",
    "Hanabi": "Marksman",
    "Claude": "Marksman",
    "Granger": "Marksman,Assassin",
    "Wanwan": "Marksman",
    "Popol & Kupa": "Marksman",
    "Brody": "Marksman",
    "Beatrix": "Marksman",
    "Natan": "Marksman,Mage",
    "Melissa": "Marksman",
    "Ixia": "Marksman",
    "Obsidia": "Marksman",
    "Irithel": "Marksman",
    "Kimmy": "Marksman,Mage",
    "Roger": "Fighter,Marksman",   # ← Roger bisa Fighter atau Marksman
    
    # === TANK ===
    "Tigreal": "Tank",
    "Akai": "Tank",
    "Franco": "Tank",
    "Minotaur": "Tank,Support",
    "Lolita": "Tank,Support",
    "Gatotkaca": "Tank",
    "Hylos": "Tank",
    "Uranus": "Tank",
    "Khufra": "Tank",
    "Baxia": "Tank",
    "Atlas": "Tank",
    "Barats": "Tank,Fighter",
    "Gloo": "Tank",
    "Edith": "Tank,Marksman",
    "Belerick": "Tank",
    "Grock": "Tank,Fighter",
    "Johnson": "Tank",
    "Jhonson": "Tank",   # fallback kalau ada typo
    
    # === SUPPORT ===
    "Rafaela": "Support,Mage",
    "Estes": "Support",
    "Diggie": "Support",
    "Kaja": "Support,Assassin",
    "Carmilla": "Support,Tank",
    "Mathilda": "Support,Assassin",
    "Floryn": "Support",
    "Faramis": "Support,Mage",
    "Angela": "Support",
    "Kalea": "Support,Tank",
    "Marcel": "Support,Tank",
    "Chip": "Support",
}


def update_roles():
    print("🚀 Mulai update role hero...")
    
    app = create_app()
    with app.app_context():
        heroes = HeroMaster.query.all()
        print(f"📊 Total hero di database: {len(heroes)}\n")
        
        updated = 0
        not_found = 0
        not_found_names = []
        
        for hero in heroes:
            # Cari case-insensitive
            role = HERO_ROLES.get(hero.name)
            if not role:
                for key, value in HERO_ROLES.items():
                    if key.lower() == hero.name.lower():
                        role = value
                        break
            
            if role:
                hero.role = role
                updated += 1
            else:
                # Default kalau gak ketemu
                hero.role = "Fighter"
                not_found += 1
                not_found_names.append(hero.name)
        
        db.session.commit()
        
        print(f"🎉 Selesai!")
        print(f"   ✅ Updated: {updated}")
        print(f"   ⚠️  Not found: {not_found}")
        
        if not_found_names:
            print(f"\n⚠️  Hero yang gak ke-mapping (pakai default 'Fighter'):")
            for name in not_found_names:
                print(f"   - {name}")
        
        print(f"\n📊 Total hero: {len(heroes)}")


if __name__ == "__main__":
    update_roles()
"""
Script seed 133 hero ML dari Rone Arena API ke tabel heroes_master.
"""

import requests
import json
from app import create_app
from models.models import db, HeroMaster


API_URL = "https://arena.rone.dev/api/heroes"


def seed_heroes():
    print("🚀 Mulai seed hero ML...")
    
    # Fetch
    try:
        params = {"size": 200, "lang": "id"}
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ Gagal fetch: {e}")
        return
    
    records = data.get("data", {}).get("records", [])
    print(f"✅ Dapet {len(records)} hero\n")
    
    # PRINT STRUKTUR HERO PERTAMA
    print("=" * 60)
    print("🔍 STRUKTUR RECORD PERTAMA:")
    print("=" * 60)
    first = records[0]
    print(json.dumps(first, indent=2)[:2500])
    print("=" * 60)
    print()
    
    # Test akses path
    print("🔍 Test akses path:")
    print(f"  rec['data']['hero']: {first.get('data', {}).get('hero') is not None}")
    hero_container = first.get("data", {}).get("hero", {})
    print(f"  hero_container keys: {list(hero_container.keys()) if isinstance(hero_container, dict) else 'NOT DICT'}")
    print(f"  hero_container.get('hero_id'): {hero_container.get('hero_id')}")
    print(f"  hero_container.get('data'): {hero_container.get('data')}")
    print()
    
    # Init app
    app = create_app()
    with app.app_context():
        db.create_all()
        
        existing = HeroMaster.query.count()
        if existing > 0:
            print(f"⚠️  Udah ada {existing} hero. Hapus dulu...")
            HeroMaster.query.delete()
            db.session.commit()
        
        created = 0
        skipped = 0
        
        for rec in records:
            hero_container = rec.get("data", {}).get("hero", {})
            hero_data = hero_container.get("data", {})
            
            hero_id = hero_container.get("hero_id")
            name = hero_data.get("name")
            head = hero_data.get("head")
            
            # Kalau hero_id None, coba cari di tempat lain
            if hero_id is None:
                # Coba dari rec langsung
                hero_id = rec.get("hero_id") or rec.get("data", {}).get("hero_id")
            
            if not name or hero_id is None:
                skipped += 1
                continue
            
            existing = HeroMaster.query.filter_by(name=name).first()
            if existing:
                skipped += 1
                continue
            
            hero = HeroMaster(id=int(hero_id), name=name, image_url=head)
            db.session.add(hero)
            created += 1
        
        db.session.commit()
        
        print(f"\n🎉 Selesai!")
        print(f"   ✅ Created: {created}")
        print(f"   ⏭️  Skipped: {skipped}")
        print(f"   📊 Total: {HeroMaster.query.count()}")


if __name__ == "__main__":
    seed_heroes()
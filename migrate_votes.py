from app import create_app
from models.models import db
from sqlalchemy import text

def migrate():
    app = create_app()
    with app.app_context():
        try:
            # Bikin tabel votes
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS votes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    clip_id INT NOT NULL,
                    vote_type INT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_user_clip (user_id, clip_id),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (clip_id) REFERENCES clips(id) ON DELETE CASCADE
                )
            """))
            db.session.commit()
            print("✅ Tabel 'votes' berhasil dibuat.")
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    migrate()
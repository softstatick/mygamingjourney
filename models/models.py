from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="gamer")  # "gamer" | "coach"
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)

    # === Data pribadi ===
    nama_lengkap = db.Column(db.String(100))
    nickname = db.Column(db.String(50))
    foto = db.Column(db.String(255))
    bio = db.Column(db.Text)

    # === Data gaming ===
    rank = db.Column(db.String(30), default="Mythic")
    game_role_1 = db.Column(db.String(30), default="Jungler")
    game_role_2 = db.Column(db.String(30), nullable=True)
    game_role_3 = db.Column(db.String(30), nullable=True)
    is_all_role = db.Column(db.Boolean, default=False)
    region = db.Column(db.String(50), default="Indonesia")
    winrate = db.Column(db.Float, default=0.0)
    total_match = db.Column(db.Integer, default=0)
    mvp = db.Column(db.Integer, default=0)
    availability = db.Column(db.String(20), default="open")

    # === Kontak (opsional) ===
    kontak_wa = db.Column(db.String(30))
    kontak_discord = db.Column(db.String(50))
    kontak_ig = db.Column(db.String(50))

    # === Relasi 1:M ===
    heroes = db.relationship("Hero", backref="profile", cascade="all, delete-orphan", lazy=True)
    clips = db.relationship("Clip", backref="profile", cascade="all, delete-orphan", lazy=True)
    achievements = db.relationship("Achievement", backref="profile", cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Profile {self.nickname}>"


class HeroMaster(db.Model):
    __tablename__ = "heroes_master"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    image_url = db.Column(db.String(500))
    role = db.Column(db.String(100))     # ← String(100) — biar bisa multi-role CSV


class Hero(db.Model):
    """Hero pool user — hero yang dikuasai player."""
    __tablename__ = "heroes"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    master_hero_id = db.Column(db.Integer, db.ForeignKey("heroes_master.id"))  # ← BARU
    winrate = db.Column(db.Float, default=0.0)
    total_match = db.Column(db.Integer, default=0)

    # Relasi ke master hero
    master = db.relationship("HeroMaster", backref="user_heroes")

    def __repr__(self):
        return f"<Hero {self.master.name if self.master else self.master_hero_id}>"


class Clip(db.Model):
    __tablename__ = "clips"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    judul = db.Column(db.String(150), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(20), nullable=True)
    video_id = db.Column(db.String(100), nullable=True)
    thumbnail = db.Column(db.String(500), nullable=True)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    report_count = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Boolean, default=False)
    deskripsi = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def vote_score(self):
        return sum(v.vote_type for v in self.votes)

class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    judul = db.Column(db.String(150), nullable=False)
    deskripsi = db.Column(db.Text)
    tanggal = db.Column(db.Date)
    foto = db.Column(db.String(255), nullable=True)


class Vote(db.Model):
    __tablename__ = "votes"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    clip_id = db.Column(db.Integer, db.ForeignKey("clips.id"), nullable=False)
    vote_type = db.Column(db.Integer, nullable=False) # 1 = upvote, -1 = downvote
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('user_id', 'clip_id', name='unique_user_clip'),)

    user = db.relationship("User", backref="votes")
    clip = db.relationship("Clip", backref="votes")
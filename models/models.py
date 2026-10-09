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
    
    # Relasi 1:1 dengan Profile
    profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model):
    __tablename__ = "profiles"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    
    # Data pribadi
    nama_lengkap = db.Column(db.String(100))
    nickname = db.Column(db.String(50))
    foto = db.Column(db.String(255))  # path file
    bio = db.Column(db.Text)
    
    # Data gaming
    rank = db.Column(db.String(30), default="Mythic")
    game_role = db.Column(db.String(30), default="Jungler")
    region = db.Column(db.String(50), default="Indonesia")
    winrate = db.Column(db.Float, default=0.0)
    total_match = db.Column(db.Integer, default=0)
    kda = db.Column(db.Float, default=0.0)
    availability = db.Column(db.String(20), default="open")  # "open" | "closed"
    
    # Kontak (opsional)
    kontak_wa = db.Column(db.String(30))
    kontak_discord = db.Column(db.String(50))
    kontak_ig = db.Column(db.String(50))
    
    # Relasi 1:M
    heroes = db.relationship("Hero", backref="profile", cascade="all, delete-orphan", lazy=True)
    clips = db.relationship("Clip", backref="profile", cascade="all, delete-orphan", lazy=True)
    achievements = db.relationship("Achievement", backref="profile", cascade="all, delete-orphan", lazy=True)
    
    def __repr__(self):
        return f"<Profile {self.nickname}>"


class Hero(db.Model):
    __tablename__ = "heroes"
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    nama_hero = db.Column(db.String(50), nullable=False)
    winrate = db.Column(db.Float, default=0.0)
    total_match = db.Column(db.Integer, default=0)


class Clip(db.Model):
    __tablename__ = "clips"
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    judul = db.Column(db.String(150), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Achievement(db.Model):
    __tablename__ = "achievements"
    
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), nullable=False)
    judul = db.Column(db.String(150), nullable=False)
    deskripsi = db.Column(db.Text)
    tanggal = db.Column(db.Date)
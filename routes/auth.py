from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User, Profile

auth_bp = Blueprint("auth", __name__)


# ============================================
# REGISTER
# ============================================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        role = request.form.get("role", "gamer")
        
        # Validasi
        if not username or not email or not password:
            session["modal"] = {
                "title": "Data Belum Lengkap",
                "message": "Semua field wajib diisi.",
                "type": "error"
            }
            return redirect(url_for("auth.register"))
        
        if len(password) < 6:
            session["modal"] = {
                "title": "Password Terlalu Pendek",
                "message": "Password minimal 6 karakter.",
                "type": "error"
            }
            return redirect(url_for("auth.register"))
        
        if password != confirm:
            session["modal"] = {
                "title": "Password Tidak Sama",
                "message": "Password dan konfirmasi harus sama.",
                "type": "error"
            }
            return redirect(url_for("auth.register"))
        
        if role not in ["gamer", "coach"]:
            role = "gamer"
        
        # Cek duplikat
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            session["modal"] = {
                "title": "Sudah Terdaftar",
                "message": "Username atau email sudah dipakai.",
                "type": "error"
            }
            return redirect(url_for("auth.register"))
        
        # Bikin user baru
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=role,
        )
        db.session.add(new_user)
        db.session.flush()
        
        # Bikin profile kosong
        new_profile = Profile(
            user_id=new_user.id,
            nickname=username,
            nama_lengkap=username,
            bio="Ceritakan perjalanan gaming kamu di sini.",
            rank="Mythic",
            game_role="Jungler",
            region="Indonesia",
            availability="open",
        )
        db.session.add(new_profile)
        db.session.commit()
        
        # Auto login
        login_user(new_user)
        
        # Set modal data
        session["modal"] = {
            "title": "Akun Berhasil Dibuat!",
            "message": f"Selamat bergabung, {username}! Portofolio kamu siap diisi.",
            "type": "success"
        }
        
        return redirect(url_for("main.home"))
    
    return render_template("auth/register.html")


# ============================================
# LOGIN
# ============================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        
        if not email or not password:
            session["modal"] = {
                "title": "Data Belum Lengkap",
                "message": "Email dan password wajib diisi.",
                "type": "error"
            }
            return redirect(url_for("auth.login"))
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            session["modal"] = {
                "title": "Login Gagal",
                "message": "Email atau password salah.",
                "type": "error"
            }
            return redirect(url_for("auth.login"))
        
        # Login sukses
        login_user(user, remember=True)
        
        # Set modal welcome
        session["modal"] = {
            "title": f"Selamat Datang, {user.username}!",
            "message": "Siap lawan siapa hari ini?",
            "type": "welcome"
        }
        
        next_page = request.args.get("next")
        if next_page:
            return redirect(next_page)
        
        return redirect(url_for("main.home"))
    
    return render_template("auth/login.html")


# ============================================
# LOGOUT
# ============================================
@auth_bp.route("/logout")
@login_required
def logout():
    username = current_user.username
    logout_user()
    
    # Set modal goodbye
    session["modal"] = {
        "title": f"Sampai Jumpa, {username}!",
        "message": "Sampai jumpa di scrim berikutnya!",
        "type": "goodbye"
    }
    
    return redirect(url_for("main.home"))
import os
import uuid
from flask import Blueprint, render_template, abort, request, redirect, url_for, session, current_app, jsonify
from flask_login import login_required, current_user
from models.models import db, Profile, User, Hero, HeroMaster, Clip, Achievement
from config import allowed_file

gamer_bp = Blueprint("gamer", __name__)


# ============================================
# VIEW PROFIL
# ============================================
@gamer_bp.route("/profile")
@login_required
def my_profile():
    if not current_user.profile:
        abort(404, "Profil belum dibuat")

    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)

    return render_template(
        "gamer/profile_view.html",
        profile=current_user.profile,
        is_owner=True,
        modal_data=modal_data,
        toast_data=toast_data
    )


@gamer_bp.route("/gamer/<int:profile_id>")
def public_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    is_owner = current_user.is_authenticated and current_user.id == profile.user_id

    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)

    return render_template(
        "gamer/profile_view.html",
        profile=profile,
        is_owner=is_owner,
        modal_data=modal_data,
        toast_data=toast_data
    )


# ============================================
# EDIT PROFIL
# ============================================
@gamer_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    profile = current_user.profile
    if not profile:
        abort(404, "Profil belum dibuat")

    if request.method == "POST":
        # Ambil data form
        nickname = request.form.get("nickname", "").strip()
        nama_lengkap = request.form.get("nama_lengkap", "").strip()
        bio = request.form.get("bio", "").strip()
        rank = request.form.get("rank", "").strip()
        game_role_1 = request.form.get("game_role_1", "").strip()
        game_role_2 = request.form.get("game_role_2", "").strip() or None
        game_role_3 = request.form.get("game_role_3", "").strip() or None
        is_all_role = request.form.get("is_all_role") == "on"
        region = request.form.get("region", "").strip()
        availability = request.form.get("availability", "open")
        kontak_wa = request.form.get("kontak_wa", "").strip() or None
        kontak_discord = request.form.get("kontak_discord", "").strip() or None
        kontak_ig = request.form.get("kontak_ig", "").strip() or None

        # Konversi angka
        try:
            winrate = float(request.form.get("winrate", 0) or 0)
        except ValueError:
            winrate = 0

        try:
            total_match = int(request.form.get("total_match", 0) or 0)
        except ValueError:
            total_match = 0

        try:
            mvp = int(request.form.get("mvp", 0) or 0)
        except ValueError:
            mvp = 0

        # Validasi
        if not nickname:
            session["modal"] = {
                "title": "Nickname Kosong",
                "message": "Nickname wajib diisi.",
                "type": "error"
            }
            return redirect(url_for("gamer.edit_profile"))

        if availability not in ["open", "closed"]:
            availability = "open"

        # === UPDATE FIELD DASAR ===
        profile.nickname = nickname
        profile.nama_lengkap = nama_lengkap or nickname
        profile.bio = bio or "Belum ada bio."
        profile.rank = rank or "Mythic"
        profile.region = region or "Indonesia"
        profile.availability = availability
        profile.winrate = max(0, min(100, winrate))
        profile.total_match = max(0, total_match)
        profile.mvp = max(0, mvp)
        profile.kontak_wa = kontak_wa
        profile.kontak_discord = kontak_discord
        profile.kontak_ig = kontak_ig

        # === LOGIC MULTI-ROLE ===
        if is_all_role:
            profile.game_role_1 = "All Role"
            profile.game_role_2 = None
            profile.game_role_3 = None
            profile.is_all_role = True
        else:
            profile.game_role_1 = game_role_1 or "Jungler"
            profile.game_role_2 = (
                game_role_2 if game_role_2 and game_role_2 != game_role_1 else None
            )
            profile.game_role_3 = (
                game_role_3
                if game_role_3 and game_role_3 != game_role_1 and game_role_3 != game_role_2
                else None
            )
            profile.is_all_role = False

               # === HERO POOL ===
        # Loop semua form key — cari yang mulai dengan "hero_data_"
        Hero.query.filter_by(profile_id=profile.id).delete()

        for key in request.form.keys():
            if not key.startswith("hero_data_"):
                continue

            # key format: "hero_data_<hero_id>"
            try:
                hero_id = int(key.replace("hero_data_", ""))
            except ValueError:
                continue

            # Ambil nilai winrate + match dari hidden field
            winrate_key = f"hero_winrate_{hero_id}"
            match_key = f"hero_match_{hero_id}"

            try:
                wr = float(request.form.get(winrate_key, 0) or 0)
            except (ValueError, TypeError):
                wr = 0

            try:
                tm = int(request.form.get(match_key, 0) or 0)
            except (ValueError, TypeError):
                tm = 0

            hero = Hero(
                profile_id=profile.id,
                master_hero_id=hero_id,
                winrate=max(0, min(100, wr)),
                total_match=max(0, tm),
            )
            db.session.add(hero)

        db.session.commit()

        session["modal"] = {
            "title": "Profil Berhasil Diupdate!",
            "message": "Perubahan kamu udah tersimpan.",
            "type": "success"
        }

        return redirect(url_for("gamer.my_profile"))

    # GET — render form
    # Ambil semua hero master + hero yang udah dipilih user
    all_heroes = HeroMaster.query.order_by(HeroMaster.name).all()
    user_heroes = {h.master_hero_id: h for h in profile.heroes}

    # Extract unique roles dari semua hero
    roles_set = set()
    for h in all_heroes:
        if h.role:
            for r in h.role.split(","):
                roles_set.add(r.strip())
    all_roles = sorted(roles_set)

    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)

    return render_template(
        "gamer/profile_edit.html",
        profile=profile,
        all_heroes=all_heroes,
        user_heroes=user_heroes,
        all_roles=all_roles,
        modal_data=modal_data,
        toast_data=toast_data
    )


# ============================================
# UPLOAD FOTO PROFIL (AJAX)
# ============================================
@gamer_bp.route("/profile/edit/photo", methods=["POST"])
@login_required
def upload_photo():
    profile = current_user.profile
    if not profile:
        return jsonify({"success": False, "message": "Profil tidak ditemukan."}), 404

    if "photo" not in request.files:
        return jsonify({"success": False, "message": "File tidak ditemukan."}), 400

    file = request.files["photo"]

    if file.filename == "":
        return jsonify({"success": False, "message": "File kosong."}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "message": "Format tidak didukung."}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    if profile.foto:
        old_path = os.path.join(upload_folder, profile.foto)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
            except:
                pass

    file.save(filepath)
    profile.foto = filename
    db.session.commit()

    foto_url = url_for("static", filename=f"uploads/{filename}")

    return jsonify({
        "success": True,
        "message": "Foto berhasil diupload!",
        "foto_url": foto_url
    })


# ============================================
# HAPUS FOTO PROFIL
# ============================================
@gamer_bp.route("/profile/edit/photo/delete", methods=["POST"])
@login_required
def delete_photo():
    profile = current_user.profile
    if not profile or not profile.foto:
        session["modal"] = {
            "title": "Tidak Ada Foto",
            "message": "Kamu belum punya foto profil.",
            "type": "error"
        }
        return redirect(url_for("gamer.edit_profile"))

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    old_path = os.path.join(upload_folder, profile.foto)
    if os.path.exists(old_path):
        try:
            os.remove(old_path)
        except:
            pass

    profile.foto = None
    db.session.commit()

    session["modal"] = {
        "title": "Foto Dihapus",
        "message": "Foto profil kamu udah dihapus.",
        "type": "success"
    }

    return redirect(url_for("gamer.edit_profile"))


# ============================================
# CLIP — Add + Delete (SIMPLE)
# ============================================
@gamer_bp.route("/profile/edit/clip", methods=["POST"])
@login_required
def add_clip():
    profile = current_user.profile
    if not profile:
        return jsonify({"success": False, "message": "Profil tidak ditemukan."}), 404
    
    judul = request.form.get("judul", "").strip()
    link = request.form.get("link", "").strip()
    
    if not judul or not link:
        return jsonify({"success": False, "message": "Judul dan link wajib diisi."}), 400
    
    # Detect platform + video_id dari link
    platform = "other"
    video_id = None
    thumbnail = None
    
    # YouTube
    if "youtube.com" in link or "youtu.be" in link:
        platform = "youtube"
        if "youtu.be/" in link:
            video_id = link.split("youtu.be/")[1].split("?")[0].split("&")[0]
        elif "watch?v=" in link:
            video_id = link.split("watch?v=")[1].split("&")[0]
        elif "shorts/" in link:
            video_id = link.split("shorts/")[1].split("?")[0]
        if video_id:
            thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    # TikTok
    elif "tiktok.com" in link:
        platform = "tiktok"
        if "/video/" in link:
            video_id = link.split("/video/")[1].split("?")[0]
    # Instagram
    elif "instagram.com" in link:
        platform = "instagram"
        if "/reel/" in link:
            video_id = link.split("/reel/")[1].split("/")[0].split("?")[0]
        elif "/p/" in link:
            video_id = link.split("/p/")[1].split("/")[0].split("?")[0]
    
    # Cek duplikat
    existing = Clip.query.filter_by(profile_id=profile.id, link=link).first()
    if existing:
        return jsonify({"success": False, "message": "Clip ini udah kamu tambahin."}), 400
    
    # Limit 10 clip
    count = Clip.query.filter_by(profile_id=profile.id).count()
    if count >= 10:
        return jsonify({"success": False, "message": "Maksimal 10 clip."}), 400
    
    clip = Clip(
        profile_id=profile.id,
        judul=judul,
        link=link,
        platform=platform,
        video_id=video_id or "unknown",
        thumbnail=thumbnail,
    )
    db.session.add(clip)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "clip_id": clip.id,
        "message": "Clip berhasil ditambahkan!",
    })


@gamer_bp.route("/profile/edit/clip/delete/<int:clip_id>", methods=["POST"])
@login_required
def delete_clip(clip_id):
    profile = current_user.profile
    if not profile:
        return jsonify({"success": False, "message": "Profil tidak ditemukan."}), 404
    
    clip = Clip.query.filter_by(id=clip_id, profile_id=profile.id).first()
    if not clip:
        return jsonify({"success": False, "message": "Clip tidak ditemukan."}), 404
    
    db.session.delete(clip)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Clip dihapus."})


# ============================================
# ACHIEVEMENT — Add + Delete (SIMPLE)
# ============================================
@gamer_bp.route("/profile/edit/achievement", methods=["POST"])
@login_required
def add_achievement():
    from datetime import datetime
    
    profile = current_user.profile
    if not profile:
        return jsonify({"success": False, "message": "Profil tidak ditemukan."}), 404
    
    judul = request.form.get("judul", "").strip()
    deskripsi = request.form.get("deskripsi", "").strip()
    tanggal_str = request.form.get("tanggal", "").strip()
    
    if not judul:
        return jsonify({"success": False, "message": "Judul wajib diisi."}), 400
    
    # Parse tanggal
    tanggal = None
    if tanggal_str:
        try:
            tanggal = datetime.strptime(tanggal_str, "%Y-%m-%d").date()
        except ValueError:
            tanggal = None
    
    # Limit 20 achievement
    count = Achievement.query.filter_by(profile_id=profile.id).count()
    if count >= 20:
        return jsonify({"success": False, "message": "Maksimal 20 achievement."}), 400
    
    ach = Achievement(
        profile_id=profile.id,
        judul=judul,
        deskripsi=deskripsi or None,
        tanggal=tanggal,
    )
    db.session.add(ach)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "achievement_id": ach.id,
        "message": "Achievement ditambahkan!",
    })


@gamer_bp.route("/profile/edit/achievement/delete/<int:ach_id>", methods=["POST"])
@login_required
def delete_achievement(ach_id):
    profile = current_user.profile
    if not profile:
        return jsonify({"success": False, "message": "Profil tidak ditemukan."}), 404
    
    ach = Achievement.query.filter_by(id=ach_id, profile_id=profile.id).first()
    if not ach:
        return jsonify({"success": False, "message": "Achievement tidak ditemukan."}), 404
    
    db.session.delete(ach)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Achievement dihapus."})


# ============================================
# BROWSE GAMER (GAMER DIRECTORY)
# ============================================
@gamer_bp.route("/browse")
def browse():
    # Ambil semua user dengan role 'gamer' yang udah punya profil
    gamers = User.query.filter_by(role='gamer').join(Profile).all()
    
    # Ambil list role & rank unik buat filter (opsional, buat nanti)
    
    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)

    return render_template(
        "gamer/browse.html", 
        gamers=gamers,
        modal_data=modal_data,
        toast_data=toast_data
    )
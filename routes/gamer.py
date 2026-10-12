import os
import uuid
from flask import Blueprint, render_template, abort, request, redirect, url_for, session, current_app, jsonify
from flask_login import login_required, current_user
from models.models import db, Profile
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
            kda = float(request.form.get("kda", 0) or 0)
        except ValueError:
            kda = 0

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
        profile.kda = max(0, kda)
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

        db.session.commit()

        session["modal"] = {
            "title": "Profil Berhasil Diupdate!",
            "message": "Perubahan kamu udah tersimpan.",
            "type": "success"
        }

        return redirect(url_for("gamer.my_profile"))

    # GET — render form
    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)

    return render_template(
        "gamer/profile_edit.html",
        profile=profile,
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
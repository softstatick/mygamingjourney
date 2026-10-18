from flask import Blueprint, render_template, session
from models.models import db, User, Profile

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)
    
    # Ambil 4 gamer dengan winrate tertinggi buat Featured Gamers
    top_gamers = User.query.filter_by(role='gamer')\
        .join(Profile)\
        .order_by(Profile.winrate.desc())\
        .limit(4)\
        .all()
        
    return render_template(
        "home.html", 
        modal_data=modal_data, 
        toast_data=toast_data,
        top_gamers=top_gamers
    )


@main_bp.route("/about")
def about():
    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)
    return render_template("about.html", modal_data=modal_data, toast_data=toast_data)


@main_bp.route("/contact")
def contact():
    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)
    return render_template("contact.html", modal_data=modal_data, toast_data=toast_data)
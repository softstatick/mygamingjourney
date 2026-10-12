from flask import Blueprint, render_template, session

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    modal_data = session.pop("modal", None)
    toast_data = session.pop("toast", None)
    return render_template("home.html", modal_data=modal_data, toast_data=toast_data)


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
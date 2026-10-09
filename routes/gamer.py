from flask import Blueprint

gamer_bp = Blueprint("gamer", __name__)

@gamer_bp.route("/test-gamer")
def test():
    return "Gamer OK"
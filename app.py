import logging

from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from models.models import db, User


# Init extensions
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- Logging ---
    level = logging.DEBUG if app.config["DEBUG"] else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
    )
    app.logger.setLevel(level)
    
    # Init database
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Init login manager
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Silakan masuk terlebih dahulu."
    login_manager.login_message_category = "warning"
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprint
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.gamer import gamer_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(gamer_bp)
    
    # Bikin folder upload kalau belum ada
    import os
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # Bikin tabel database kalau belum ada
    with app.app_context():
        db.create_all()

    # --- Error handlers + logging ---

    @app.errorhandler(404)
    def not_found(e):
        app.logger.warning("404 Not Found on %s", request.path)
        return render_template("error/404.html", error=e), 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.exception("500 Internal Server Error on %s", request.path)
        return render_template("error/500.html", error=e), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=Config.DEBUG, port=Config.PORT)
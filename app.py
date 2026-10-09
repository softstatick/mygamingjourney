from flask import Flask
from flask_login import LoginManager
from config import Config
from models.models import db, User


# Init extensions
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Init database
    db.init_app(app)
    
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
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config.config import Config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Silakan login terlebih dahulu.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Setup user_loader
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import main
    from app.auth import bp as auth_bp
    from app.dashboard import bp as dashboard_bp
    from app.barang import bp as barang_bp
    from app.kategori import bp as kategori_bp
    from app.merk import bp as merk_bp
    from app.transaksi import bp as transaksi_bp
    from app.kontrak import bp as kontrak_bp
    from app.laporan import laporan_bp
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(barang_bp)
    app.register_blueprint(kategori_bp)
    app.register_blueprint(merk_bp)
    app.register_blueprint(transaksi_bp)
    app.register_blueprint(kontrak_bp)
    app.register_blueprint(laporan_bp)
    
    return app

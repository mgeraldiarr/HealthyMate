from flask import Flask # flask itu untuk membuat aplikasi web
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from .models import db, User

def create_app():
    app = Flask(__name__) # app itu WSGI application (standar python untuk menghubungkan aplikasi web dengan server web), Flask itu framework, __name__ itu nama file ini

    # Konfigurasi Secret Key untuk session security
    app.config['SECRET_KEY'] = 'htymte300526'

    # Konfigurasi Database MySQL (ganti root & password dengan milik Anda)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/healthymate_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inisialisasi db dan ekstensi lainnya
    db.init_app(app)
    Migrate(app, db) # Inisialisasi Flask-Migrate
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'app_routes.login' # Akan diarahkan ke sini jika belum login

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import app_routes
    app.register_blueprint(app_routes)

    # --- Perintah Seeder ---
    @app.cli.command("seed-db")
    def seed_db():
        """Membuat data awal untuk admin dan dokter."""
        
        # Cek apakah dokter dengan id=1 sudah ada
        doctor1 = User.query.filter_by(id=1).first()
        if doctor1:
            print("Pengguna dengan ID 1 sudah ada. Mengupdate role menjadi 'doctor'.")
            doctor1.role = 'doctor'
            doctor1.name = 'Andini Putri' # Sesuaikan nama jika perlu
        else:
            print("Membuat pengguna dokter baru dengan ID 1...")
            # Membuat dokter dengan ID spesifik
            doctor1 = User(
                id=1,
                username='dr.andini',
                email='doctor1@healthymate.com',
                password_hash=generate_password_hash('doctor123', method='pbkdf2:sha256'),
                role='doctor',
                name='Andini Putri'
            )
            db.session.add(doctor1)

            # Cek apakah dokter dengan id=2 sudah ada
        doctor2 = User.query.filter_by(id=2).first()
        if doctor2:
            print("Pengguna dengan ID 2 sudah ada. Mengupdate role menjadi 'doctor'.")
            doctor2.role = 'doctor'
            doctor2.name = 'Budi Santoso' # Sesuaikan nama jika perlu
        else:
            print("Membuat pengguna dokter baru dengan ID 2...")
            # Membuat dokter dengan ID spesifik
            doctor2 = User(
                id=2,
                username='dr.budi',
                email='doctor2@healthymate.com',
                password_hash=generate_password_hash('doctor123', method='pbkdf2:sha256'),
                role='doctor',
                name='Budi Santoso'
            )
            db.session.add(doctor2)

        # Membuat admin (jika belum ada)
        if not User.query.filter_by(email='admin@healthymate.com').first():
            print("Membuat pengguna admin baru...")
            admin = User(
                username='admin',
                email='admin@healthymate.com',
                password_hash=generate_password_hash('admin123', method='pbkdf2:sha256'),
                role='admin',
                name='Admin HealthyMate'
            )
            db.session.add(admin)

        db.session.commit()
        print("Database seeding selesai.")

    return app

app = create_app()
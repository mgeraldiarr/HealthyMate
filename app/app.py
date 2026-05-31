from flask import Flask # flask itu untuk membuat aplikasi web
from routes import app_routes  # mengimpor app_routes dari file routes.py
from models import db
from flask_login import LoginManager

app = Flask(__name__) # app itu WSGI application (standar python untuk menghubungkan aplikasi web dengan server web), Flask itu framework, __name__ itu nama file ini

# Konfigurasi Secret Key untuk session security
app.config['SECRET_KEY'] = 'htymte300526'

# Konfigurasi Database MySQL (ganti root & password dengan milik Anda)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/healthymate_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi db dan login manager
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'app_routes.login' # Akan diarahkan ke sini jika belum login

app.register_blueprint(app_routes)  # mendaftarkan blueprint ke dalam aplikasi flask. blueprint juga di gunakan untuk mengorganisir kode aplikasi web menjadi modul modul terpisah agar ketika menjadi poyek yang besar mudah untuk maintanace

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Otomatis membuat tabel jika belum ada di database MySQL
    app.run(
        debug=True,
        # host='0.0.0.0',
        port=8000,
        # threaded=True,
    )
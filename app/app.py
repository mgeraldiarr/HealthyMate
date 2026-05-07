from flask import Flask # flask itu untuk membuat aplikasi web
from routes import app_routes  # mengimpor app_routes dari file routes.py

app = Flask(__name__) # app itu WSGI application (standar python untuk menghubungkan aplikasi web dengan server web), Flask itu framework, __name__ itu nama file ini
app.register_blueprint(app_routes)  # mendaftarkan blueprint ke dalam aplikasi flask. blueprint juga di gunakan untuk mengorganisir kode aplikasi web menjadi modul modul terpisah agar ketika menjadi poyek yang besar mudah untuk maintanace

if __name__ == '__main__':
    app.run(
        debug=True,
        # host='0.0.0.0',
        # port=8000,
        # threaded=True,
    )
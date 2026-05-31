# HealthyMate

HealthyMate adalah aplikasi web berbasis Flask yang digunakan untuk mengelola fitur kesehatan, data pengguna, dan kebutuhan aplikasi berbasis database. Project ini menggunakan Python, Flask, MySQL, serta beberapa library pendukung seperti Flask-SQLAlchemy, Flask-Login, PyMySQL, Pandas, NumPy, Matplotlib, dan Requests.

## Teknologi yang Digunakan

- Python 3
- Flask 2.2.2
- Werkzeug 2.2.3
- Flask-SQLAlchemy
- Flask-Login
- PyMySQL
- MySQL
- Pandas
- NumPy
- Matplotlib
- Requests

## Struktur Singkat Project

```bash
HealthyMate/
├── app/
│   ├── app.py
│   ├── routes/
│   ├── models/
│   ├── templates/
│   └── static/
├── venv/
├── requirements.txt
└── README.md
```

> Catatan: Folder `venv/` biasanya tidak perlu di-upload ke GitHub karena dapat dibuat ulang oleh setiap developer.

## 1. Masuk ke Folder Project

Buka terminal, lalu masuk ke folder utama project:

```bash
cd "/Users/macbook/Documents/Web Dev/HealthyMate"
```

Sesuaikan path di atas dengan lokasi project di laptop masing-masing.

## 2. Buat Virtual Environment

Untuk developer baru yang pertama kali menjalankan project, buat virtual environment terlebih dahulu:

```bash
python3 -m venv venv
```

Virtual environment digunakan agar dependency project tidak tercampur dengan package Python global di komputer.

## 3. Aktifkan Virtual Environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Jika berhasil, biasanya terminal akan menampilkan tanda seperti ini:

```bash
(venv)
```

## 4. Install Dependency dari requirements.txt

Setelah virtual environment aktif, install semua dependency project menggunakan:

```bash
pip install -r requirements.txt
```

Isi `requirements.txt` yang digunakan:

```txt
Flask==2.2.2
Werkzeug==2.2.3
Flask-SQLAlchemy
Flask-Login
PyMySQL

pandas==1.5.3
matplotlib==3.6.2
numpy==1.23.5
requests==2.28.1
```

## 5. Siapkan Database MySQL

Pastikan MySQL sudah berjalan, lalu masuk ke MySQL:

```bash
mysql -u root -p
```

Buat database untuk project:

```sql
CREATE DATABASE healthymate_db;
SHOW DATABASES;
EXIT;
```

Pastikan nama database sama dengan konfigurasi database yang ada di project, misalnya:

```python
mysql+pymysql://root:password@localhost/healthymate_db
```

Jika password MySQL kosong, biasanya formatnya bisa seperti:

```python
mysql+pymysql://root:@localhost/healthymate_db
```

## 6. Jalankan Project Flask

Masuk ke folder `app`:

```bash
cd app
```

Lalu jalankan aplikasi:

```bash
python3 app.py
```

Jika berhasil, terminal akan menampilkan pesan seperti:

```bash
* Serving Flask app 'app'
* Running on http://127.0.0.1:8000/
```

Buka browser dan akses:

```text
http://127.0.0.1:8000/
```

## Perintah Ringkas untuk Menjalankan Project

Jika project sudah pernah di-setup sebelumnya:

```bash
cd "/Users/macbook/Documents/Web Dev/HealthyMate"
source venv/bin/activate
pip install -r requirements.txt
cd app
python3 app.py
```

## Perintah Lengkap untuk Developer Baru

Jika baru pertama kali mendapatkan project:

```bash
cd "/Users/macbook/Documents/Web Dev/HealthyMate"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
python3 app.py
```

Untuk Windows:

```bash
cd "lokasi\folder\HealthyMate"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd app
python app.py
```

## Troubleshooting

### 1. Error: No module named flask_sqlalchemy

Artinya dependency belum terinstall. Jalankan:

```bash
pip install -r requirements.txt
```

Pastikan virtual environment sudah aktif sebelum menjalankan perintah tersebut.

### 2. Error: No module named flask_login

Jalankan ulang:

```bash
pip install -r requirements.txt
```

### 3. Error: Unknown database 'healthymate_db'

Artinya database belum dibuat di MySQL. Buat database dengan perintah:

```sql
CREATE DATABASE healthymate_db;
```

### 4. Error terkait Werkzeug

Jika muncul error kompatibilitas Flask dan Werkzeug, pastikan `requirements.txt` menggunakan:

```txt
Flask==2.2.2
Werkzeug==2.2.3
```

Lalu install ulang:

```bash
pip install -r requirements.txt
```

### 5. Virtual environment belum aktif

Jika dependency sudah diinstall tetapi masih error, kemungkinan terminal belum masuk ke virtual environment. Aktifkan kembali:

```bash
source venv/bin/activate
```

atau untuk Windows:

```bash
venv\Scripts\activate
```

## Catatan untuk GitHub

Agar folder virtual environment tidak ikut ter-upload ke repository, tambahkan `venv/` ke file `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc
.env
```

## Penutup

Setelah semua dependency terinstall, database dibuat, dan Flask berhasil dijalankan, aplikasi HealthyMate dapat diakses melalui browser di alamat:

```text
http://127.0.0.1:8000/
```

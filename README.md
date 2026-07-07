# HealthyMate
 
HealthyMate adalah aplikasi web berbasis Flask yang digunakan untuk mengelola fitur kesehatan, data pengguna, dan kebutuhan aplikasi berbasis database. Project ini menggunakan Python, Flask, MySQL, serta beberapa library pendukung seperti Flask-SQLAlchemy, Flask-Login, PyMySQL, Pandas, NumPy, Matplotlib, dan Requests.
 
## Teknologi yang Digunakan
 
- Python 3
- Flask 2.2.2
- Werkzeug 2.2.3
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- pytz
- PyMySQL
- MySQL
- Pandas
- NumPy
- Matplotlib
- Requests
## Struktur Singkat Project
 
```bash
HealthyMate/
├── app/               # Folder utama aplikasi (Python Package)
│   ├── __init__.py    # Titik masuk package, membuat instance Flask
│   ├── routes.py      # Definisi semua URL/endpoint
│   ├── models.py      # Definisi tabel database
│   ├── templates/
│   └── static/
├── run.py             # File untuk menjalankan server
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
Flask-Migrate
pytz
 
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
 
## 6. Jalankan Migrasi Database
 
Setelah database dibuat, jalankan perintah migrasi dari direktori root project untuk membuat semua tabel yang diperlukan sesuai dengan model yang ada di `app/models.py`.
 
```bash
flask db upgrade
```
 
Perintah ini akan membuat tabel `users`, `progress`, `appointments`, dan `messages`.
 
## 7. Isi Data Awal (Seeding)
 
Project ini memerlukan data awal (seperti akun admin dan dokter) agar bisa berfungsi dengan baik. Jalankan perintah seeder berikut dari direktori root:
 
```bash
flask seed-db
```
 
Perintah ini akan membuat:
- 1 akun admin (email: admin@healthymate.com, pass: admin123)
- 2 akun dokter (dr. Andini & dr. Budi)
## 8. Jalankan Project Flask
 
Pastikan Anda berada di direktori **root** project (`HealthyMate/`), bukan di dalam folder `app/`.
 
Lalu jalankan aplikasi menggunakan file `run.py`:
 
```bash
python3 run.py # atau 'python run.py' di Windows
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
 
## Alur Kerja Lengkap untuk Developer Baru
 
Berikut adalah ringkasan perintah dari awal hingga akhir untuk setup project di lingkungan baru (misal: macOS/Linux).
 
```bash
cd "/Users/macbook/Documents/Web Dev/HealthyMate"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE healthymate_db;"
flask db upgrade
flask seed-db
python3 run.py
```
 
Untuk Windows:
 
```bash
cd "lokasi\folder\HealthyMate"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE healthymate_db;"
flask db upgrade
flask seed-db
python run.py
```
 
## Alur Kerja Harian
 
Untuk menjalankan project yang sudah pernah di-setup sebelumnya, cukup jalankan dari direktori **root**:
 
```bash
cd "/Users/macbook/Documents/Web Dev/HealthyMate"
source venv/bin/activate
python3 run.py
```
 
## Alur Kerja Saat Mengubah Model Database
 
Setiap kali Anda mengubah file `app/models.py` (misalnya menambah tabel atau kolom), ikuti alur `Flask-Migrate` berikut:
 
1. **Generate script migrasi baru:**
```bash
   flask db migrate -m "Deskripsi singkat perubahan, misal: Add phone_number to User"
```
2. **Terapkan perubahan ke database:**
```bash
   flask db upgrade
```
 
Setelah itu, informasikan kepada tim Anda agar mereka juga menjalankan `flask db upgrade` di lingkungan masing-masing untuk menyamakan struktur database.
 
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
 
Setelah semua dependency terinstall, database dibuat, migrasi dijalankan, dan data awal di-seed, aplikasi HealthyMate dapat diakses melalui browser di alamat:
 
```text
http://127.0.0.1:8000/
```
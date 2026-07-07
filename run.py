from app import app

if __name__ == '__main__':
    # Port 8000 digunakan agar tidak bentrok dengan service lain
    app.run(debug=True, port=8000)
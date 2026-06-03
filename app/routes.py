from flask import Blueprint, render_template, request, redirect, url_for, flash # request untuk mengakses data dari form (POST,GET) || renden_template unutk render HTML temlate
from services.meal_recommendation import MealRecommendation # mengimport mealrecommendation dari services.meal_recommendation
from services.calorie_calculator import CalorieCalculator # mengimport caloriecalculator dari services.calorie_calculator
from models import db, User, Progress
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

app_routes = Blueprint('app_routes', __name__)

# == Rute Halaman Statis ==

@app_routes.route('/')
def home():
    return render_template('home.html')

@app_routes.route('/about')
def about():
    return render_template('about.html')

@app_routes.route('/consultation')
def consultation():
    return render_template('consultation.html')

@app_routes.route('/services')
def services():
    return render_template('services.html')

# == Rute Otentikasi (Login/Register) ==

@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('app_routes.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Cek apakah email atau username sudah ada
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            flash('Email address already exists.', 'danger')
            return redirect(url_for('app_routes.register'))

        # Buat user baru dengan password yang di-hash
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)

        # Simpan ke database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('app_routes.login'))

    return render_template('auth/register.html')

@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app_routes.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        # Cek user dan password
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('app_routes.login'))

        login_user(user) # Daftarkan user ke session login
        return redirect(url_for('app_routes.dashboard'))

    return render_template('auth/login.html')


# == Rute Kalkulator dan Dashboard ==

@app_routes.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    if request.method == 'POST':
        user_data = request.form
        try:
            # ini adalah untuk ambil data user dari form
            weight = float(user_data.get('berat', 0))
            height = float(user_data.get('tinggi', 0))
            age = int(user_data.get('usia', 0))
            gender = user_data.get('gender', 'male')
            activity_level = user_data.get('aktivitas', 'sedentary')
            tujuan = user_data.get('tujuan', 'jaga')

            # ini untuk validasi data yang di inputkan
            if not all([weight, height, age]):
                raise ValueError("All fields are required")

            # ini untuk menghitung bmr dan tdee
            calorie_calculator = CalorieCalculator(weight, height, age, gender, activity_level)
            bmr = calorie_calculator.calculate_bmr()
            tdee = calorie_calculator.calculate_calories()

            # ini adalah untuk kalori yang dibutuhkan
            if tujuan == 'turun':
                result = "Recommended calories for deficit (weight loss)"
                tdee -= 500
            elif tujuan == 'naik':
                result = "Recommended calories for surplus (weight gain)"
                tdee += 500
            else:
                result = "Recommended calories to maintain weight"

            # ini adalah rekomendasi makanan acak
            meal_recommender = MealRecommendation()
            meal_plan = meal_recommender.get_random_meal_plan()

            meal_data = {
                'breakfast': meal_plan.get('breakfast', {}),
                'lunch': meal_plan.get('lunch', {}),
                'dinner': meal_plan.get('dinner', {})
            }
            
            new_progress = Progress(
                user_id=current_user.id,
                weight=weight,
                height=height,
                tdee_result=tdee,
                tujuan=tujuan
            )
            db.session.add(new_progress)
            db.session.commit()

            return render_template('calculator.html',
                                   bmr=bmr,
                                   tdee=tdee,
                                   result=result,
                                   meal_type=meal_data,
                                   error=None)

        except ValueError as e:  
            error = "All fields must be filled in correctly."
            return render_template('calculator.html',
                                    error=error,
                                    bmr=None,
                                    tdee=None,
                                    result=None,
                                    meal_type=None)

    return render_template('calculator.html',
                           error=None,
                           bmr=None,
                           tdee=None,
                           result=None,
                           meal_type=None)

@app_routes.route('/dashboard')
@login_required # Hanya user yang sudah login yang bisa akses
def dashboard():
    bmr = None
    tdee = None
    if current_user.weight and current_user.height and current_user.age and current_user.gender and current_user.activity_level:
        calorie_calculator = CalorieCalculator(current_user.weight, current_user.height, current_user.age, current_user.gender, current_user.activity_level)
        bmr = calorie_calculator.calculate_bmr()
        tdee = calorie_calculator.calculate_calories()

    progress_records = Progress.query.filter_by(user_id=current_user.id).order_by(Progress.date.desc()).limit(5).all()
    
    return render_template('dashboard.html', bmr=bmr, tdee=tdee, progress_records=progress_records)

@app_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('app_routes.home'))

@app_routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        
        # Mengambil data int/float dan mengubahnya jika ada nilainya
        age_str = request.form.get('age')
        weight_str = request.form.get('weight')
        height_str = request.form.get('height')
        
        current_user.age = int(age_str) if age_str else None
        current_user.weight = float(weight_str) if weight_str else None
        current_user.height = float(height_str) if height_str else None
        current_user.gender = request.form.get('gender')
        current_user.activity_level = request.form.get('activity_level')
        
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('app_routes.profile'))
        
    return render_template('profile.html')

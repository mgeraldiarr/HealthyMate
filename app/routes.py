from flask import Blueprint, render_template, request, redirect, url_for, flash # request untuk mengakses data dari form (POST,GET) || renden_template unutk render HTML temlate
from .services.meal_recommendation import MealRecommendation # mengimport mealrecommendation dari services.meal_recommendation
from .services.calorie_calculator import CalorieCalculator # mengimport caloriecalculator dari services.calorie_calculator
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Progress, Appointment, Message
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

# Buat Blueprint
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

@app_routes.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')

@app_routes.route('/contact-us')
def contact_us():
    return render_template('contact_us.html')


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

@app_routes.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Email ditemukan, lanjut ke langkah 2
            return redirect(url_for('app_routes.reset_password_step2', email=email))
        else:
            flash('Email address not found. Please check and try again.', 'danger')
            return redirect(url_for('app_routes.forgot_password'))
    return render_template('auth/forgot_password_step1.html')

@app_routes.route('/reset-password-step2/<email>', methods=['GET', 'POST'])
def reset_password_step2(email):
    user = User.query.filter_by(email=email).first_or_404()
    if request.method == 'POST':
        username = request.form.get('username')
        if user.username == username:
            # Username cocok, lanjut ke langkah 3
            return redirect(url_for('app_routes.reset_password_step3', user_id=user.id))
        else:
            flash('Username does not match the provided email.', 'danger')
            return redirect(url_for('app_routes.reset_password_step2', email=email))
    return render_template('auth/forgot_password_step2.html', email=email)

@app_routes.route('/reset-password-step3/<int:user_id>', methods=['GET', 'POST'])
def reset_password_step3(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('app_routes.reset_password_step3', user_id=user_id))

        # Update password
        user.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        db.session.commit()

        flash('Your password has been successfully updated! Please log in.', 'success')
        return redirect(url_for('app_routes.login'))
    return render_template('auth/forgot_password_step3.html', user_id=user_id)

@app_routes.route('/appointment/make/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def make_appointment(doctor_id):
    # Pastikan user yang diakses adalah dokter
    doctor = User.query.filter_by(id=doctor_id, role='doctor').first_or_404()

    # Cek apakah user sudah punya appointment 'pending' dengan dokter ini
    existing_pending_appointment = Appointment.query.filter_by(
        user_id=current_user.id,
        doctor_id=doctor_id,
        status='pending'
    ).first()

    # Jika sudah ada appointment pending, tampilkan halaman info dan jangan proses form
    if existing_pending_appointment:
        return render_template('make_appointment.html', 
                               doctor=doctor, 
                               existing_pending_appointment=existing_pending_appointment)

    if request.method == 'POST':
        slot_str = request.form.get('appointment_slot')
        phone_number = request.form.get('phone_number')
        complaint = request.form.get('complaint')

        if not slot_str or not phone_number:
            flash('Please select a schedule and fill in your contact number.', 'danger')
            return redirect(url_for('app_routes.make_appointment', doctor_id=doctor_id))

        appointment_time = datetime.fromisoformat(slot_str)

        # Buat appointment baru dengan status 'pending'
        new_appointment = Appointment(
            user_id=current_user.id,
            doctor_id=doctor.id,
            appointment_time=appointment_time,
            phone_number=phone_number,
            complaint=complaint,
            status='pending'
        )
        db.session.add(new_appointment)
        db.session.commit()

        flash(f'Your appointment request for Dr. {doctor.name} has been sent and is pending approval.', 'success')
        return redirect(url_for('app_routes.make_appointment', doctor_id=doctor_id))

    # --- Logika untuk GET request ---

    # Simulasi jadwal dokter (nantinya bisa disimpan di database)
    # Format: {hari_dalam_bahasa_inggris: [jam_mulai, jam_selesai]}
    schedules = {
        1: {'Monday': [9, 12], 'Wednesday': [9, 12], 'Saturday': [13, 15]},
        2: {'Tuesday': [13, 16], 'Thursday': [13, 16], 'Friday': [10, 12]}
    }
    doctor_schedule = schedules.get(doctor.id, {})

    # Ambil appointment yang sudah di-approve untuk 7 hari ke depan
    today = datetime.utcnow().date()
    next_week = today + timedelta(days=7)
    booked_slots = {apt.appointment_time for apt in Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.status == 'approved',
        Appointment.appointment_time >= datetime.combine(today, datetime.min.time()),
        Appointment.appointment_time < datetime.combine(next_week, datetime.min.time())
    ).all()}

    # Generate slot waktu yang tersedia
    available_slots = {}
    for i in range(7):
        current_day = today + timedelta(days=i)
        day_name = current_day.strftime('%A')
        if day_name in doctor_schedule:
            start_hour, end_hour = doctor_schedule[day_name]
            day_slots = []
            for hour in range(start_hour, end_hour):
                slot_time = datetime(current_day.year, current_day.month, current_day.day, hour)
                day_slots.append({
                    'iso_format': slot_time.isoformat(),
                    'time': slot_time.strftime('%H:%M'),
                    'available': slot_time not in booked_slots
                })
            if day_slots:
                available_slots[current_day.strftime('%A, %d %b %Y')] = day_slots

    return render_template('make_appointment.html', doctor=doctor, available_slots=available_slots, existing_pending_appointment=None)


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

    # Ambil appointment yang akan datang atau sedang berlangsung
    now = datetime.utcnow()
    user_appointments = (
    Appointment.query
    .options(joinedload(Appointment.doctor))
    .filter(
        Appointment.user_id == current_user.id,
        Appointment.status == 'approved',
        Appointment.appointment_time >= now - timedelta(hours=1)
    )
    .order_by(Appointment.appointment_time.asc())
    .limit(3)
    .all()
)

    progress_records = Progress.query.filter_by(user_id=current_user.id).order_by(Progress.date.desc()).limit(5).all()
    
    return render_template('dashboard.html', bmr=bmr, tdee=tdee, progress_records=progress_records, appointments=user_appointments, now=now)

@app_routes.route('/history')
@login_required
def history():
    # Ambil semua catatan progress untuk pengguna saat ini, diurutkan dari yang terbaru
    all_progress = Progress.query.filter_by(user_id=current_user.id).order_by(Progress.date.desc()).all()
    return render_template('history.html', progress_records=all_progress)

@app_routes.route('/my-appointments')
@login_required
def my_appointments():
    now = datetime.utcnow()

    appointments = (
        Appointment.query
        .options(joinedload(Appointment.doctor))
        .filter_by(user_id=current_user.id)
        .order_by(Appointment.appointment_time.desc())
        .all()
    )

    return render_template(
        "my_appointments.html",
        appointments=appointments,
        now=now,
        timedelta=timedelta
    )

@app_routes.route('/appointment/chat/<int:appointment_id>')
@login_required
def chat_room(appointment_id):
    # Gunakan joinedload untuk memuat data dokter secara efisien bersamaan dengan appointment
    appointment = Appointment.query.options(
        joinedload(Appointment.doctor)
    ).filter_by(id=appointment_id, user_id=current_user.id).first_or_404()
    
    return render_template('chat_room.html', appointment=appointment)

@app_routes.route('/history/delete', methods=['POST'])
@login_required
def delete_history():
    # Ambil daftar ID dari form yang dikirim
    ids_to_delete = request.form.getlist('record_ids')
    
    if not ids_to_delete:
        flash('No items selected for deletion.', 'warning')
        return redirect(url_for('app_routes.history'))

   # Hapus record yang dimiliki oleh user saat ini
    Progress.query.filter(
        Progress.id.in_(ids_to_delete),
        Progress.user_id == current_user.id
    ).delete(synchronize_session=False)
    db.session.commit()
    flash('Selected records have been removed.', 'success')
    return redirect(url_for('app_routes.history'))

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

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort # request untuk mengakses data dari form (POST,GET) || renden_template unutk render HTML temlate
from .services.meal_recommendation import MealRecommendation # mengimport mealrecommendation dari services.meal_recommendation
from .services.calorie_calculator import CalorieCalculator # mengimport caloriecalculator dari services.calorie_calculator
from collections import defaultdict
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Progress, Appointment, Message
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import datetime, timedelta, timezone
import pytz

# Buat Blueprint
app_routes = Blueprint('app_routes', __name__)

# --- Decorator untuk Role-based Access ---
def role_forbidden(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.role == role:
                abort(403)  # Forbidden for this specific role
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# == Rute Halaman Statis ==

@app_routes.route('/')
@role_forbidden('admin')
def home():
    return render_template('home.html')

@app_routes.route('/about')
@role_forbidden('admin')
def about():
    return render_template('about.html')

@app_routes.route('/consultation')
@role_forbidden('doctor')
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

        if user.role == 'admin':
            return redirect(url_for('app_routes.admin_dashboard'))
        elif user.role == 'doctor':
            return redirect(url_for('app_routes.doctor_dashboard'))
        else:
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
    1: {
        'Monday': ['09:00', '10:00', '11:05'],
        'Wednesday': ['09:00', '13:30'],
        'Saturday': ['13:00', '14:30']
    },
    2: {
        'Tuesday': ['13:00', '14:00', '15:30'],
        'Thursday': ['13:00', '14:00', '15:00'],
        'Friday': ['08:53', '11:05']
    }
}
    doctor_schedule = schedules.get(doctor.id, {})

    now = datetime.now()

    today = now.date() # Gunakan tanggal dari waktu lokal yang sudah ditentukan
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
        day_name = current_day.strftime("%A")

        if day_name in doctor_schedule:
            day_slots = []

            for time_str in doctor_schedule[day_name]:
                hour, minute = map(int, time_str.split(":"))

                slot_time = datetime(
                    current_day.year,
                    current_day.month,
                    current_day.day,
                    hour,
                    minute
                )

                if slot_time > now:
                    day_slots.append({
                        "iso_format": slot_time.isoformat(),
                        "time": slot_time.strftime("%H:%M"),
                        "available": slot_time not in booked_slots
                    })

            if day_slots:
                available_slots[current_day.strftime("%A, %d %b %Y")] = day_slots

    return render_template('make_appointment.html', doctor=doctor, available_slots=available_slots, existing_pending_appointment=None)


# == Rute Kalkulator dan Dashboard ==

@app_routes.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)

    # Ambil semua appointment yang masih pending dari semua dokter
    pending_appointments = Appointment.query.options(joinedload(Appointment.patient), joinedload(Appointment.doctor)).filter(Appointment.status == 'pending').order_by(Appointment.created_at.asc()).all()
    return render_template('admin_dashboard.html', pending_appointments=pending_appointments)

@app_routes.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    if current_user.role != 'doctor':
        abort(403)

    # Jadwal dokter yang di-hardcode (sama seperti di make_appointment)
    schedules = {
        1: {'Monday', 'Wednesday', 'Saturday'},
        2: {'Tuesday', 'Thursday', 'Friday'}
    }
    doctor_schedule_days = schedules.get(current_user.id, set())

    now = datetime.now()
    today = now.date()

    # Logika untuk mengubah status appointment yang sudah lewat menjadi 'expired'
    expired_appointments = Appointment.query.filter(
        Appointment.doctor_id == current_user.id,
        Appointment.status == 'approved',
        Appointment.appointment_time < now - timedelta(hours=1)
    ).all()
    if expired_appointments:
        for appt in expired_appointments:
            appt.status = 'expired'
        db.session.commit()
    
    # Ambil janji temu yang akan datang dan yang sedang aktif (dimulai dalam 1 jam terakhir) untuk dokter ini
    upcoming_appointments_list = Appointment.query.options(
        joinedload(Appointment.patient)
    ).filter(
        Appointment.doctor_id == current_user.id,
        Appointment.status == 'approved',
        Appointment.appointment_time >= now - timedelta(hours=1)
    ).order_by(Appointment.appointment_time.asc()).all()

    # Kelompokkan janji temu yang akan datang berdasarkan tanggal untuk pencarian cepat
    appointments_by_date = defaultdict(list)
    for appt in upcoming_appointments_list:
        appointments_by_date[appt.appointment_time.date()].append(appt)

    # Tentukan awal minggu (Senin)
    start_of_week = today - timedelta(days=today.weekday())
    
    # Siapkan data untuk hari-hari dalam minggu ini yang sesuai dengan jadwal dokter
    days_to_show = []
    for i in range(7): # Loop untuk 7 hari dalam seminggu
        current_day_date = start_of_week + timedelta(days=i)
        day_name = current_day_date.strftime("%A")

        # Hanya tampilkan hari jika ada dalam jadwal dokter DAN hari itu adalah hari ini atau di masa depan
        if day_name in doctor_schedule_days and current_day_date >= today:
            appointments_on_day = appointments_by_date.get(current_day_date, [])
            days_to_show.append((current_day_date, appointments_on_day))

    return render_template(
        'doctor_dashboard.html', 
        days_to_show=days_to_show,
        timedelta=timedelta,
        now=datetime.now
    )


@app_routes.route('/calculator', methods=['GET', 'POST'])
@login_required
@role_forbidden('doctor')
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
    if current_user.role == 'doctor':
        return redirect(url_for('app_routes.doctor_dashboard'))

    bmr = None
    tdee = None
    if current_user.weight and current_user.height and current_user.age and current_user.gender and current_user.activity_level:
        calorie_calculator = CalorieCalculator(current_user.weight, current_user.height, current_user.age, current_user.gender, current_user.activity_level)
        bmr = calorie_calculator.calculate_bmr()
        tdee = calorie_calculator.calculate_calories()

    now = datetime.now()

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
    
    return render_template(
        'dashboard.html', 
        bmr=bmr, 
        tdee=tdee, 
        progress_records=progress_records, 
        appointments=user_appointments, 
        now=now,
        timedelta=timedelta
    )

@app_routes.route('/history')
@login_required
@role_forbidden('doctor')
def history():
    # Ambil semua catatan progress untuk pengguna saat ini, diurutkan dari yang terbaru
    all_progress = Progress.query.filter_by(user_id=current_user.id).order_by(Progress.date.desc()).all()
    return render_template('history.html', progress_records=all_progress)

@role_forbidden('doctor')
@app_routes.route('/my-appointments')
@login_required
def my_appointments():
    now = datetime.now()

    # Logika untuk mengubah status appointment yang sudah lewat menjadi 'expired' (setelah 1 jam dari jadwal)
    # Hanya periksa appointment milik user yang sedang login
    expired_appointments = Appointment.query.filter(
        Appointment.user_id == current_user.id,
        Appointment.status == 'approved',
        Appointment.appointment_time < now - timedelta(hours=1)
    ).all()

    if expired_appointments:
        for appt in expired_appointments:
            appt.status = 'expired'
        db.session.commit()
        flash('Beberapa janji temu yang telah lewat ditandai sebagai kedaluwarsa.', 'info')


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

@app_routes.route('/appointment/handle/<int:appointment_id>', methods=['POST'])
@login_required
def handle_appointment(appointment_id):
    if current_user.role != 'admin':
        abort(403)

    appointment = Appointment.query.options(joinedload(Appointment.patient)).filter_by(id=appointment_id).first_or_404()
    action = request.form.get('action')

    if action == 'approve':
        appointment.status = 'approved'
        flash(f'Appointment with {appointment.patient.name or appointment.patient.username} has been approved.', 'success')
    elif action == 'reject':
        appointment.status = 'rejected'
        flash(f'Appointment with {appointment.patient.name or appointment.patient.username} has been rejected.', 'info')
    
    db.session.commit()
    return redirect(url_for('app_routes.admin_dashboard'))

@app_routes.route('/appointment/chat/<int:appointment_id>')
@login_required
def chat_room(appointment_id):
    # Gunakan joinedload untuk memuat data dokter dan pasien secara efisien bersamaan dengan appointment
    appointment = Appointment.query.options(
        joinedload(Appointment.doctor),
        joinedload(Appointment.patient)
    ).filter(
        Appointment.id == appointment_id,
        (Appointment.user_id == current_user.id) | (Appointment.doctor_id == current_user.id)
    ).first_or_404()

    now = datetime.now()
    # Tentukan apakah chat aktif: status 'approved' dan waktu sekarang berada dalam rentang 1 jam dari jadwal
    is_chat_active = (
        appointment.status == 'approved' and
        now >= appointment.appointment_time and
        now < appointment.appointment_time + timedelta(hours=1)
    )

    # Ambil semua pesan untuk appointment ini
    messages = Message.query.filter_by(appointment_id=appointment.id).order_by(Message.timestamp.asc()).all()
    
    return render_template('chat_room.html', 
                           appointment=appointment, 
                           messages=messages, 
                           is_chat_active=is_chat_active)

@app_routes.route('/appointment/chat/<int:appointment_id>/read', methods=['POST'])
@login_required
def read_messages(appointment_id):
    # Tandai semua pesan yang diterima oleh current_user di chat ini sebagai 'read'
    messages_to_read = Message.query.filter(
        Message.appointment_id == appointment_id,
        Message.sender_id != current_user.id, # Hanya pesan dari orang lain
        Message.is_read == False
    ).all()

    for msg in messages_to_read:
        msg.is_read = True
    
    db.session.commit()

    return jsonify({'status': 'success', 'message': f'{len(messages_to_read)} messages marked as read.'})

@app_routes.route('/appointment/chat/<int:appointment_id>/send', methods=['POST'])
@login_required
def send_message(appointment_id):
    # Pastikan user adalah bagian dari appointment ini (pasien atau dokter)
    appointment = Appointment.query.filter(
        Appointment.id == appointment_id,
        ((Appointment.user_id == current_user.id) | (Appointment.doctor_id == current_user.id))
    ).first_or_404()

    # Tambahan: Pastikan pesan hanya bisa dikirim selama sesi chat aktif
    now = datetime.now()
    is_chat_active = (
        appointment.status == 'approved' and
        now >= appointment.appointment_time and
        now < appointment.appointment_time + timedelta(hours=1)
    )
    if not is_chat_active:
        return jsonify({'status': 'error', 'message': 'Chat session is not active.'}), 403

    content = request.form.get('content')
    if not content:
        return jsonify({'status': 'error', 'message': 'Message cannot be empty.'}), 400

    new_message = Message(
        appointment_id=appointment_id,
        sender_id=current_user.id,
        content=content
    )
    db.session.add(new_message)
    db.session.commit()

    # Kembalikan data pesan yang baru dibuat dalam format JSON
    return jsonify({
        'status': 'success',
        'message': {
            'sender_id': new_message.sender_id,
            'content': new_message.content,
            'timestamp': new_message.timestamp.strftime('%H:%M'),
            'is_read': False # Pesan baru defaultnya belum dibaca
        }
    })
@app_routes.route('/history/delete', methods=['POST'])
@login_required
@role_forbidden('doctor')
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
        # Common fields for all roles
        current_user.name = request.form.get('name') or current_user.name
        current_user.gender = request.form.get('gender')

        # Fields specific to 'user' role
        if current_user.role == 'user':
            age_str = request.form.get('age')
            weight_str = request.form.get('weight')
            height_str = request.form.get('height')
            
            current_user.age = int(age_str) if age_str else None
            current_user.weight = float(weight_str) if weight_str else None
            current_user.height = float(height_str) if height_str else None
            current_user.activity_level = request.form.get('activity_level')
        
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('app_routes.profile'))
        
    return render_template('profile.html')

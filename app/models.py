# # Dengan SQLAlchemy (ORM)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     weight = db.Column(db.Float)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


# class User:
#     def __init__(self, name, age, weight, height, activity_level):
#         self.name = name
#         self.age = age
#         self.weight = weight
#         self.height = height
#         self.activity_level = activity_level

# Inisialisasi SQLAlchemy
db = SQLAlchemy()


# class Meal:
#     def __init__(self, name, calories, ingredients):
#         self.name = name
#         self.calories = calories
#         self.ingredients = ingredients

# Tabel untuk menyimpan data akun pengguna
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    role = db.Column(db.String(20), nullable=False, default='user') # 'user', 'doctor', 'admin'
    # Data Profil Pengguna
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    gender = db.Column(db.String(20))
    activity_level = db.Column(db.String(50))

    # Relasi ke tabel Progress (1 User punya banyak Progress)
    progress_history = db.relationship('Progress', backref='user', lazy=True, cascade="all, delete-orphan")
    # Relasi untuk appointment
    appointments = db.relationship('Appointment', foreign_keys='Appointment.user_id', backref='patient', lazy=True)


# class MealRecommendation:
#     def __init__(self):
#         self.meals = []

#     def add_meal(self, meal):
#         self.meals.append(meal)

#     def get_meals(self):
#         return self.meals

# class CaloricNeeds:
#     def __init__(self, user):
#         self.user = user

#     def calculate_bmr(self):
#         if self.user.gender == 'male':
#             return 10 * self.user.weight + 6.25 * self.user.height - 5 * self.user.age + 5
#         else:
#             return 10 * self.user.weight + 6.25 * self.user.height - 5 * self.user.age - 161

#     def calculate_daily_calories(self):
#         bmr = self.calculate_bmr()
#         activity_multiplier = {
#             'sedentary': 1.2,
#             'lightly active': 1.375,
#             'moderately active': 1.55,
#             'very active': 1.725,
#             'super active': 1.9
#         }
#         return bmr * activity_multiplier.get(self.user.activity_level, 1.2)


# Tabel untuk mencatat riwayat tracker pengguna di Dashboard
class Progress(db.Model):
    __tablename__ = 'progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    tdee_result = db.Column(db.Float)
    tujuan = db.Column(db.String(20)) # misal: 'turun', 'naik', 'jaga'

# Tabel untuk menyimpan data appointment
class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, approved, rejected, completed, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    phone_number = db.Column(db.String(20), nullable=True)
    complaint = db.Column(db.Text, nullable=True)
    doctor_notes = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    doctor = db.relationship('User', foreign_keys=[doctor_id])

# Tabel untuk menyimpan pesan chat
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_whatsapp_button = db.Column(db.Boolean, default=False) # Flag untuk pesan khusus tombol WA
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    sender = db.relationship('User', foreign_keys=[sender_id])
    appointment = db.relationship('Appointment', backref='messages', lazy=True)


# Tabel untuk menyimpan notifikasi pengguna
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(30), nullable=False, default='general') # 'appointment', 'admin_manual', 'schedule'
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    link = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True, cascade="all, delete-orphan"))


class DoctorSchedule(db.Model):
    __tablename__ = 'doctor_schedules'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    day_of_week = db.Column(db.String(20), nullable=False) # 'Monday', 'Tuesday', etc.
    time_slot = db.Column(db.String(5), nullable=False) # '09:00', '15:30', etc.
    effective_from = db.Column(db.Date, nullable=True)
    effective_to = db.Column(db.Date, nullable=True)

    doctor = db.relationship('User', foreign_keys=[doctor_id], backref=db.backref('schedules', lazy=True, cascade="all, delete-orphan"))


class ScheduleProposal(db.Model):
    __tablename__ = 'schedule_proposals'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending') # 'pending', 'approved', 'rejected'
    proposed_schedule = db.Column(db.Text, nullable=False) # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    admin_notes = db.Column(db.Text, nullable=True)
    effective_date = db.Column(db.Date, nullable=True)

    doctor = db.relationship('User', foreign_keys=[doctor_id], backref=db.backref('schedule_proposals', lazy=True, cascade="all, delete-orphan"))

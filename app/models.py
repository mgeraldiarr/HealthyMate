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
    
    # Data Profil Pengguna
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    gender = db.Column(db.String(20))
    activity_level = db.Column(db.String(50))

    # Relasi ke tabel Progress (1 User punya banyak Progress)
    progress_history = db.relationship('Progress', backref='user', lazy=True, cascade="all, delete-orphan")


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
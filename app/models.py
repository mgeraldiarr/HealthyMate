# # Dengan SQLAlchemy (ORM)
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     weight = db.Column(db.Float)

# class User:
#     def __init__(self, name, age, weight, height, activity_level):
#         self.name = name
#         self.age = age
#         self.weight = weight
#         self.height = height
#         self.activity_level = activity_level

# class Meal:
#     def __init__(self, name, calories, ingredients):
#         self.name = name
#         self.calories = calories
#         self.ingredients = ingredients

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
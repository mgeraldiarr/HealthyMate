from flask import Blueprint, render_template, request # request untuk mengakses data dari form (POST,GET) || renden_template unutk render HTML temlate
from services.meal_recommendation import MealRecommendation # mengimport mealrecommendation dari services.meal_recommendation
from services.calorie_calculator import CalorieCalculator # mengimport caloriecalculator dari services.calorie_calculator

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def home():
    return render_template('home.html')

@app_routes.route('/about')
def about():
    return render_template('about.html')

@app_routes.route('/consultation')
def consultation():
    return render_template('consultation.html')

@app_routes.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app_routes.route('/calories', methods=['GET', 'POST'])
def calories():
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

            return render_template('calories.html',
                                   bmr=bmr,
                                   tdee=tdee,
                                   result=result,
                                   meal_type=meal_data,
                                   error=None)

        except ValueError as e:  
            error = "All fields must be filled in correctly."
            return render_template('calories.html',
                                    error=error,
                                    bmr=None,
                                    tdee=None,
                                    result=None,
                                    meal_type=None)

    return render_template('calories.html',
                           error=None,
                           bmr=None,
                           tdee=None,
                           result=None,
                           meal_type=None)

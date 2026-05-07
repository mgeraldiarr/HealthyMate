class CalorieCalculator:
    # ini adalah konstruktor untuk inisialisasi data user
    def __init__(self, weight, height, age, gender, activity_level):
        self.weight = weight  # in kilograms
        self.height = height  # in centimeters
        self.age = age  # in years
        self.gender = gender  # 'male' or 'female'
        self.activity_level = activity_level  # activity level factor

    # ini adalah menghitung bmr menggunakan rumus Mifflin St. Jeor 
    def calculate_bmr(self):
        if self.gender == 'male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        return bmr
    
    # ini adalah untuk menghitung total kalori harian tdee berdasarkan level aktivitas
    def calculate_calories(self):
        bmr = self.calculate_bmr()

        activity_factors = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'high': 1.725,
            'extreme': 1.9
        }
        factor = activity_factors.get(self.activity_level, 1.2)

        daily_calories = bmr * factor
        return daily_calories
import random

# ini adalah list daftar makanan untuk sarapan, siang, dan malam berserta kalori nya 
class MealRecommendation:
    def __init__(self):
        self.meals = {
            "breakfast": [
                {"name": "Oatmeal with fruits and chia seeds", "calories": 250},
                {"name": "Whole grain toast with avocado", "calories": 300},
                {"name": "Greek yogurt parfait with granola", "calories": 350},
                {"name": "Scrambled eggs with spinach", "calories": 220},
                {"name": "Smoothie bowl with berries and almonds", "calories": 280},
            ],
            "lunch": [
                {"name": "Grilled chicken breast with quinoa and broccoli", "calories": 500},
                {"name": "Grilled salmon with brown rice and asparagus", "calories": 550},
                {"name": "Turkey sandwich with whole grain bread and salad", "calories": 450},
                {"name": "Vegetable stir-fry with tofu and basmati rice", "calories": 480},
                {"name": "Chickpea and spinach salad with lemon dressing", "calories": 400},
            ],
            "dinner": [
                {"name": "Baked cod with roasted sweet potatoes", "calories": 500},
                {"name": "Grilled chicken with zucchini noodles", "calories": 450},
                {"name": "Beef stew with carrots and peas", "calories": 550},
                {"name": "Shrimp stir-fry with mixed vegetables", "calories": 480},
                {"name": "Stuffed bell peppers with ground turkey and quinoa", "calories": 520},
            ],
        }

    # ini untuk mengembalikan rekomendasi makanan berdasarkan jenis makanannya 
    def get_recommendations(self, meal_type):
        return self.meals.get(meal_type, [])

    # Menghasilkan 1 menu acak untuk tiap waktu makan
    def get_random_meal_plan(self):
        """Menghasilkan 1 menu acak untuk tiap waktu makan"""
        return {
            "breakfast": random.choice(self.meals["breakfast"]),
            "lunch": random.choice(self.meals["lunch"]),
            "dinner": random.choice(self.meals["dinner"]),
        }


# import random
# from typing import Dict, List, Optional, Union

# class MealRecommendation:
#     def __init__(self):
#         self.meals = {
#             "breakfast": [
#                 {"name": "Oatmeal with fruits and chia seeds", "calories": 250, "protein": 8, "carbs": 45, "fat": 5, "category": "vegetarian"},
#                 {"name": "Whole grain toast with avocado", "calories": 300, "protein": 10, "carbs": 35, "fat": 12, "category": "vegetarian"},
#                 {"name": "Greek yogurt parfait with granola", "calories": 350, "protein": 15, "carbs": 40, "fat": 10, "category": "vegetarian"},
#                 {"name": "Scrambled eggs with spinach", "calories": 220, "protein": 18, "carbs": 5, "fat": 15, "category": "vegetarian"},
#                 {"name": "Smoothie bowl with berries and almonds", "calories": 280, "protein": 12, "carbs": 30, "fat": 8, "category": "vegan"},
#             ],
#             "lunch": [
#                 {"name": "Grilled chicken breast with quinoa and broccoli", "calories": 500, "protein": 40, "carbs": 45, "fat": 12, "category": "high-protein"},
#                 {"name": "Grilled salmon with brown rice and asparagus", "calories": 550, "protein": 35, "carbs": 50, "fat": 20, "category": "high-protein"},
#                 {"name": "Turkey sandwich with whole grain bread and salad", "calories": 450, "protein": 30, "carbs": 40, "fat": 15, "category": "balanced"},
#                 {"name": "Vegetable stir-fry with tofu and basmati rice", "calories": 480, "protein": 20, "carbs": 60, "fat": 10, "category": "vegetarian"},
#                 {"name": "Chickpea and spinach salad with lemon dressing", "calories": 400, "protein": 15, "carbs": 50, "fat": 12, "category": "vegan"},
#             ],
#             "dinner": [
#                 {"name": "Baked cod with roasted sweet potatoes", "calories": 500, "protein": 35, "carbs": 40, "fat": 15, "category": "low-carb"},
#                 {"name": "Grilled chicken with zucchini noodles", "calories": 450, "protein": 42, "carbs": 20, "fat": 18, "category": "low-carb"},
#                 {"name": "Beef stew with carrots and peas", "calories": 550, "protein": 38, "carbs": 35, "fat": 25, "category": "high-protein"},
#                 {"name": "Shrimp stir-fry with mixed vegetables", "calories": 480, "protein": 30, "carbs": 30, "fat": 20, "category": "low-carb"},
#                 {"name": "Stuffed bell peppers with ground turkey and quinoa", "calories": 520, "protein": 32, "carbs": 45, "fat": 18, "category": "balanced"},
#             ],
#         }
        
#         self.dietary_categories = {
#             "vegetarian": ["vegetarian", "vegan"],
#             "vegan": ["vegan"],
#             "high-protein": ["high-protein"],
#             "low-carb": ["low-carb"],
#             "balanced": ["balanced"]
#         }

#     def get_recommendations(self, meal_type: str, category: Optional[str] = None) -> List[Dict]:
#         """Get meal recommendations for a specific meal type and optional category"""
#         meals = self.meals.get(meal_type, [])
#         if category:
#             meals = [meal for meal in meals if meal.get("category") in self.dietary_categories.get(category, [])]
#         return meals

#     def get_random_meal_plan(self, category: Optional[str] = None) -> Dict[str, Dict]:
#         """Generate a random meal plan with optional dietary category filter"""
#         plan = {}
#         for meal_type in ["breakfast", "lunch", "dinner"]:
#             options = self.get_recommendations(meal_type, category)
#             if options:
#                 plan[meal_type] = random.choice(options)
#         return plan

#     def get_meal_by_calories(self, max_calories: int) -> Dict[str, List[Dict]]:
#         """Get meals filtered by maximum calories per meal"""
#         result = {}
#         for meal_type, meals in self.meals.items():
#             filtered = [meal for meal in meals if meal["calories"] <= max_calories]
#             if filtered:
#                 result[meal_type] = filtered
#         return result

#     def calculate_daily_nutrition(self, meal_plan: Dict[str, Dict]) -> Dict[str, int]:
#         """Calculate total nutrition for a given meal plan"""
#         totals = {
#             "calories": 0,
#             "protein": 0,
#             "carbs": 0,
#             "fat": 0
#         }
        
#         for meal in meal_plan.values():
#             totals["calories"] += meal["calories"]
#             totals["protein"] += meal["protein"]
#             totals["carbs"] += meal["carbs"]
#             totals["fat"] += meal["fat"]
            
#         return totals
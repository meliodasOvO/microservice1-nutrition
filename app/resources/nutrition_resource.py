# nutrition_resource.py
from app.models.nutrition import Nutrition
from fastapi import HTTPException
from app.services.service_factory import ServiceFactory

class NutritionResource:
    @staticmethod
    def get_nutrition(recipe_id: int):
        conn = ServiceFactory.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM nutrition WHERE recipe_id = %s", (recipe_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Nutrition information not found")
            return result
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_nutrition(nutrition: Nutrition):
        conn = ServiceFactory.get_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO nutrition (recipe_id, calories, carbohydrates, fiber, fat, sugar, sodium, ingredient_alternatives)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                nutrition.recipe_id, nutrition.calories, nutrition.carbohydrates,
                nutrition.fiber, nutrition.fat, nutrition.sugar,
                nutrition.sodium, nutrition.ingredient_alternatives
            ))
            conn.commit()
            nutrition_id = cursor.lastrowid
        finally:
            cursor.close()
            conn.close()
        return nutrition

    @staticmethod
    def update_nutrition(recipe_id: int, nutrition: Nutrition):
        conn = ServiceFactory.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM nutrition WHERE recipe_id = %s", (recipe_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Nutrition information not found")

            query = """
                UPDATE nutrition
                SET calories = %s, carbohydrates = %s, fiber = %s, fat = %s,
                    sugar = %s, sodium = %s, ingredient_alternatives = %s
                WHERE recipe_id = %s
            """
            cursor.execute(query, (
                nutrition.calories, nutrition.carbohydrates, nutrition.fiber,
                nutrition.fat, nutrition.sugar, nutrition.sodium,
                nutrition.ingredient_alternatives, recipe_id
            ))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
        return nutrition

    @staticmethod
    def delete_nutrition(recipe_id: int):
        conn = ServiceFactory.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM nutrition WHERE recipe_id = %s", (recipe_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Nutrition information not found")

            cursor.execute("DELETE FROM nutrition WHERE recipe_id = %s", (recipe_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
        return {"detail": "Nutrition information deleted successfully"}

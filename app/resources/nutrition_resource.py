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
    def get_nutrition_suggestions(offset=0, limit=10, min_calories=None, max_calories=None, diet_type=None, goal=None):
      conn = ServiceFactory.get_connection()
      cursor = conn.cursor(dictionary=True)
      try:
        query = "SELECT * FROM nutrition WHERE 1=1"
        params = []

        if min_calories is not None:
          query += " AND calories >= %s"
          params.append(min_calories)
        if max_calories is not None:
          query += " AND calories <= %s"
          params.append(max_calories)
        if diet_type is not None:
          query += " AND diet_type = %s"
          params.append(diet_type)
        if goal is not None:
          query += " AND goal = %s"
          params.append(goal)

        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(query, params)
        result = cursor.fetchall()
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
                INSERT INTO nutrition (recipe_id, calories, carbohydrates, protein, fiber, fat, sugar, sodium,
                                       ingredient_alternatives, diet_type, goal)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                nutrition.recipe_id, nutrition.calories, nutrition.carbohydrates, nutrition.protein,
                nutrition.fiber, nutrition.fat, nutrition.sugar, nutrition.sodium,
                nutrition.ingredient_alternatives, nutrition.diet_type, nutrition.goal
            ))
            conn.commit()
            nutrition_id = cursor.lastrowid
        finally:
            cursor.close()
            conn.close()
        # 返回包含生成的 nutrition_id 的对象
        return {**nutrition.dict(), "nutrition_id": nutrition_id}

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
                SET calories = %s, carbohydrates = %s, protein = %s, fiber = %s, fat = %s,
                    sugar = %s, sodium = %s, ingredient_alternatives = %s, diet_type = %s, goal = %s
                WHERE recipe_id = %s
            """
            cursor.execute(query, (
                nutrition.calories, nutrition.carbohydrates, nutrition.protein, nutrition.fiber,
                nutrition.fat, nutrition.sugar, nutrition.sodium,
                nutrition.ingredient_alternatives, nutrition.diet_type, nutrition.goal, recipe_id
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


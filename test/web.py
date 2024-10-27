from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# 数据库配置
config = {
  'user': 'root',
  'password': 'dbuserdbuser',
  'host': '35.196.59.220',
  'database': 'nutrition_db'
}


# 更新后的数据模型
class Nutrition(BaseModel):
  recipe_id: int
  calories: float
  carbohydrates: float
  fiber: float
  fat: float
  sugar: float
  sodium: float
  ingredient_alternatives: str


# GET 请求: 获取指定 recipe_id 的营养信息
@app.get("/nutrition/{recipe_id}")
async def get_nutrition(recipe_id: int):
  try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM nutrition WHERE recipe_id = %s"
    cursor.execute(query, (recipe_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
      return result
    else:
      raise HTTPException(status_code=404, detail="Nutrition information not found")
  except mysql.connector.Error as err:
    raise HTTPException(status_code=500, detail=str(err))


# POST 请求: 添加新的营养信息
@app.post("/nutrition")
async def create_nutrition(nutrition: Nutrition):
  try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    query = """
            INSERT INTO nutrition (recipe_id, calories, carbohydrates, fiber, fat, sugar, sodium, ingredient_alternatives)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    cursor.execute(query, (
      nutrition.recipe_id, nutrition.calories, nutrition.carbohydrates, nutrition.fiber,
      nutrition.fat, nutrition.sugar, nutrition.sodium, nutrition.ingredient_alternatives
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return nutrition
  except mysql.connector.Error as err:
    raise HTTPException(status_code=400, detail="Error inserting record: " + str(err))


# PUT 请求: 更新指定 recipe_id 的营养信息
@app.put("/nutrition/{recipe_id}")
async def update_nutrition(recipe_id: int, nutrition: Nutrition):
  try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM nutrition WHERE recipe_id = %s", (recipe_id,))
    if not cursor.fetchone():
      cursor.close()
      conn.close()
      raise HTTPException(status_code=404, detail="Nutrition information not found")

    query = """
            UPDATE nutrition
            SET calories = %s, carbohydrates = %s, fiber = %s, fat = %s, sugar = %s, sodium = %s, ingredient_alternatives = %s
            WHERE recipe_id = %s
        """
    cursor.execute(query, (
      nutrition.calories, nutrition.carbohydrates, nutrition.fiber, nutrition.fat,
      nutrition.sugar, nutrition.sodium, nutrition.ingredient_alternatives, recipe_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return nutrition
  except mysql.connector.Error as err:
    raise HTTPException(status_code=500, detail="Error updating record: " + str(err))


# DELETE 请求: 删除指定 recipe_id 的营养信息
@app.delete("/nutrition/{recipe_id}")
async def delete_nutrition(recipe_id: int):
  try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM nutrition WHERE recipe_id = %s", (recipe_id,))
    if not cursor.fetchone():
      cursor.close()
      conn.close()
      raise HTTPException(status_code=404, detail="Nutrition information not found")

    cursor.execute("DELETE FROM nutrition WHERE recipe_id = %s", (recipe_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"detail": "Nutrition information deleted successfully"}
  except mysql.connector.Error as err:
    raise HTTPException(status_code=500, detail="Error deleting record: " + str(err))

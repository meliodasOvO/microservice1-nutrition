from fastapi import APIRouter, HTTPException
from app.models.nutrition import Nutrition
from app.resources.nutrition_resource import NutritionResource

router = APIRouter()

@router.get("/nutrition/{recipe_id}", tags=["nutrition"])
async def get_nutrition_info(recipe_id: int):
    return NutritionResource.get_nutrition(recipe_id)

@router.post("/nutrition", tags=["nutrition"])
async def create_nutrition_info(nutrition: Nutrition):
    return NutritionResource.create_nutrition(nutrition)

@router.put("/nutrition/{recipe_id}", tags=["nutrition"])
async def update_nutrition_info(recipe_id: int, nutrition: Nutrition):
    return NutritionResource.update_nutrition(recipe_id, nutrition)

@router.delete("/nutrition/{recipe_id}", tags=["nutrition"])
async def delete_nutrition_info(recipe_id: int):
    return NutritionResource.delete_nutrition(recipe_id)

from fastapi import APIRouter, HTTPException, status
from app.models.nutrition import Nutrition
from app.resources.nutrition_resource import NutritionResource

router = APIRouter()

@router.get("/nutrition/{recipe_id}", tags=["nutrition"])
async def get_nutrition_info(recipe_id: int):
    result = NutritionResource.get_nutrition(recipe_id)
    if not result:
        raise HTTPException(status_code=404, detail="Nutrition information not found")
    return result

@router.post("/nutrition", tags=["nutrition"], status_code=status.HTTP_201_CREATED)
async def create_nutrition_info(nutrition: Nutrition):
    created_nutrition = NutritionResource.create_nutrition(nutrition)
    return {"message": "Nutrition information created successfully", "data": created_nutrition}

@router.put("/nutrition/{recipe_id}", tags=["nutrition"])
async def update_nutrition_info(recipe_id: int, nutrition: Nutrition):
    updated_nutrition = NutritionResource.update_nutrition(recipe_id, nutrition)
    if not updated_nutrition:
        raise HTTPException(status_code=404, detail="Nutrition information not found")
    return {"message": "Nutrition information updated successfully", "data": updated_nutrition}

@router.delete("/nutrition/{recipe_id}", tags=["nutrition"])
async def delete_nutrition_info(recipe_id: int):
    result = NutritionResource.delete_nutrition(recipe_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Nutrition information not found")
    return {"message": "Nutrition information deleted successfully"}


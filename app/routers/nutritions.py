from fastapi import APIRouter, HTTPException, status, Query
from app.models.nutrition import Nutrition
from app.resources.nutrition_resource import NutritionResource
from typing import Optional, List

router = APIRouter()

@router.get("/nutrition/{recipe_id}", tags=["nutrition"])
async def get_nutrition_info(recipe_id: int):
    result = NutritionResource.get_nutrition(recipe_id)
    if not result:
        raise HTTPException(status_code=404, detail="Nutrition information not found")
    return result

@router.get("/nutrition", tags=["nutrition"])
async def get_nutrition_list(
    page: int = Query(1, ge=1),
    min_calories: Optional[float] = None,
    max_calories: Optional[float] = None,
    diet_type: Optional[str] = None
):
    # 计算 offset 和 limit
    page_size = 2
    offset = (page - 1) * page_size
    nutrition_list = NutritionResource.get_nutrition_list(
        offset=offset,
        limit=page_size,
        min_calories=min_calories,
        max_calories=max_calories,
        diet_type=diet_type
    )
    return nutrition_list


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


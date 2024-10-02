from fastapi import APIRouter

from app.models.nutrition import NutritionInfo
from app.resources.nutrition_resource import NutritionResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/nutrition/{name}", tags=["nutrition"])
async def get_nutrition_info(name: str) -> NutritionInfo:

    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("NutritionResource")
    result = res.get_by_key(name)
    return result

@router.put("/nutrition/{name}", tags=["nutrition"])
async def update_nutrition(name: str, nutrition: NutritionInfo) -> NutritionInfo:
    res = ServiceFactory.get_service("NutritionResource")
    update_data = nutrition.dict(exclude_unset=True)
    result = res.update_by_key(name, update_data)
    return result


@router.delete("/nutrition/{name}", tags=["nutrition"])
async def delete_nutrition(name: str):
    res = ServiceFactory.get_service("NutritionResource")
    res.delete_by_key(name)
    return {"message": f"Nutrition with name {name} has been deleted"}

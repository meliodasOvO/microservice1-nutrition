from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class NutritionInfo(BaseModel):
    recipe_id: Optional[int] = None
    name:str
    calories: Optional[int] = None
    protein: Optional[float] = None  # grams
    fat: Optional[float] = None  # grams
    carbohydrates: Optional[float] = None  # grams
    sugar: Optional[float] = None  # grams


    class Config:
        json_schema_extra = {
            "example": {
                "recipe_id": 1,
                "name": "Spaghetti_Bolognese",
                "calories": 400,
                "protein": 20.5,
                "fat": 15.0,
                "carbohydrates": 45.0,
                "sugar": 8.0
            }
        }

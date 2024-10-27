from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Nutrition(BaseModel):
  recipe_id: int
  calories: float
  carbohydrates: float
  protein: float
  fiber: float
  fat: float
  sugar: float
  sodium: float
  ingredient_alternatives: str
  diet_type: str
  goal: str

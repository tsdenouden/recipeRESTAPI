from typing import Optional, List
from uuid import UUID, uuid4
from pydantic import BaseModel


# Extra information on the recipe
class RecipeMeta(BaseModel):
    credit: str = "A Human Being"
    description: str = "Delicious food that is edible & cooked."
    time: str = "A reasonable amount of time."
    rating: str = "5 stars"


# Recipe
class Recipe(BaseModel):
    id: Optional[UUID] = uuid4()
    name: str = "John Doe"
    ingredients: List[str] = ["Item1", "Item2", "Item3"]
    image: str = "URL to an image"
    calories: float = 200.0
    meta: Optional[RecipeMeta]


# Update Recipe
class UpdateRecipe(Recipe):
    __annotations__ = {k: Optional[v] for k, v in Recipe.__annotations__.items()}

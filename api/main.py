from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from models.models import Recipe, UpdateRecipe, RecipeMeta
import uvicorn

# Swagger Docs
description = """
![Drink svg](api/assets/drink@3x.png)
Helps you keep track of your recipes.

### Recipes
* Read all saved recipes
* Read a specific recipe
* Save a new recipe
* Update an existing recipe
"""

# Tags metadata
title = ["Commands"]
tags_metadata = [
    {
        "name": "Commands",
        "description": "API Endpoints"
    },
    {
        "name": "Root",
        "description": "Redirect to SwaggerUI Docs"
    }
]

app = FastAPI(
    title="Tristan's Recipe API",
    version="v1",
    description=description,
    contact={
        "name": "Tristan Shawn den Ouden",
        "url": "https://github.com/tsdenouden",
        "email": "trisdo687@gmail.com"
    },
    openapi_tags=tags_metadata,
)

# Database
db: List[Recipe] = [
    Recipe(
        id="6366b41f-b57f-4544-8364-2365c622790d",
        name="Test Dish",
        ingredients=['Foo', 'Bar', 'Baz'],
        image='https://avatars.githubusercontent.com/u/16963366',
        calories=1.618,
        meta=RecipeMeta(
            credit="Tristan",
            description="Hello, World!",
            time="20 minutes",
            rating="5 stars"
        )
    )
]


# API Endpoints

# Root, redirect to docs page
@app.get("/", tags=["Root"], summary="Redirect to documentation.")
async def root():
    response = RedirectResponse(url='/docs')
    return response


# Fetch all recipes from db
@app.get("/api/recipes", tags=["Commands"], summary="Fetch all recipes.")
async def fetch_recipes():
    return db


# Fetch a specific recipe
@app.get("/api/recipes/{recipe_id}", tags=["Commands"], summary="Fetch a recipe.")
async def fetch_recipes(recipe_id: UUID):
    for recipe in db:
        if recipe.id == recipe_id:
            return recipe
    raise HTTPException(
        status_code=404,
        detail=f"Recipe with id: {recipe_id} does not exist!"
    )


# Add a new recipe
@app.post("/api/recipes", tags=["Commands"], summary="Add a new recipe.")
async def new_recipe(recipe: Recipe):
    db.append(recipe)
    recipe.id = uuid4()
    return {"id": recipe.id}


# Delete a specific recipe
@app.delete("/api/recipes/{recipe_id}", tags=["Commands"], summary="Delete the given recipe.")
async def delete_recipe(recipe_id: UUID):
    for recipe in db:
        if recipe.id == recipe_id:
            db.remove(recipe)
            return f"Recipe with id: {recipe_id} has been deleted."
    raise HTTPException(
        status_code=404,
        detail=f"Recipe with id: {recipe_id} does not exist!"
    )


# Update a recipe
@app.put("/api/recipes/{recipe_id}", tags=["Commands"], summary="Update a recipe")
async def update_recipe(recipe_update: UpdateRecipe, recipe_id: UUID):
    for recipe in db:
        if recipe.id == recipe_id:
            if recipe_update.name is not None:
                recipe.name = recipe_update.name
            if recipe_update.ingredients is not None:
                recipe.ingredients = recipe_update.ingredients
            if recipe_update.image is not None:
                recipe.image = recipe_update.image
            if recipe_update.calories is not None:
                recipe.calories = recipe_update.calories
            if recipe_update.meta is not None:
                recipe.meta = recipe_update.meta
            return f"Recipe with id: {recipe_id} has been successfully updated."
    raise HTTPException(
        status_code=404,
        detail=f"Recipe with id: {recipe_id} does not exist!"
    )


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host="0.0.0.0")

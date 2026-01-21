from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import Recipe, RecipeCreate, RecipeRead
from app.auth import get_current_user
from app.models import User

router = APIRouter(prefix="/recipes", tags=["recipes"])

#List all recipes
@router.get("/", response_model=List[Recipe])
def read_recipes(session: Session = Depends(get_session)):
    recipes = session.exec(select(Recipe)).all()
    return recipes

#Create a new recipe
@router.post("/", response_model=RecipeRead)
def create_recipe(
    recipe: RecipeCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_recipe = Recipe(
        **recipe.dict(),
        owner_id=current_user.id
    )

    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)

    return db_recipe

#Get a specific recipe by ID
@router.get("/{recipe_id}", response_model=RecipeRead)
def read_recipe(
    recipe_id: int,
    session: Session = Depends(get_session)
):
    recipe = session.get(Recipe, recipe_id)
    
    #check if recipe exists
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe

#Update a recipe
@router.put("/{recipe_id}", response_model=RecipeRead)
def update_recipe(
    recipe_id: int,
    recipe_update: RecipeCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    recipe = session.get(Recipe, recipe_id)
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    #update recipe fields
    for key, value in recipe_update.dict().items():
        setattr(recipe, key, value)

    session.add(recipe)
    session.commit()
    session.refresh(recipe)

    return recipe

#Delete a recipe
@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    recipe = session.get(Recipe, recipe_id)

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(recipe)
    session.commit()

    return {"message": "Recipe deleted successfully"}
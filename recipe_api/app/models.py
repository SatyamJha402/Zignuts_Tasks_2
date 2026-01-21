from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

#User models
class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)

#User model with relationship to recipes
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    recipes: List["Recipe"] = Relationship(back_populates="owner")

#User models for creating and reading users
class UserCreate(UserBase):
    password: str
class UserRead(UserBase):
    id: int

#Recipe models
class RecipeBase(SQLModel):
    title: str
    description: Optional[str] = None
    ingredients: str
    steps: str
    image_path: Optional[str] = None

#Recipe model with relationship to user
class Recipe(RecipeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="recipes")

#Recipe models for creating and reading recipes
class RecipeCreate(RecipeBase):
    pass
class RecipeRead(RecipeBase):
    id: int
    owner_id: int
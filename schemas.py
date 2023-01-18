from typing import List
import uuid
from pydantic import BaseModel


class MenuBaseSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class CreateMenuSchema(MenuBaseSchema):
    pass


class MenuResponse(MenuBaseSchema):
    id: uuid.UUID


class UpdateMenuSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuResponse4List(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class ListMenuResponse(BaseModel):
    menus: List[MenuResponse4List]


class FilteredMenuResponse(MenuBaseSchema):
    id: uuid.UUID


class SubmenuBaseSchema(BaseModel):
    title: str
    description: str
    menu_id: uuid.UUID | None = None

    class Config:
        orm_mode = True


class CreateSubmenuSchema(SubmenuBaseSchema):
    pass


class SubmenuResponse(SubmenuBaseSchema):
    id: uuid.UUID


class UpdateSubmenuSchema(BaseModel):
    title: str
    description: str
    menu_id: uuid.UUID | None = None

    class Config:
        orm_mode = True


class SubmenuResponse4List(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    dishes_count: int


class ListSubmenuResponse(BaseModel):
    submenus: List[SubmenuResponse4List]


class FilteredSubmenuResponse(SubmenuBaseSchema):
    id: uuid.UUID


class DishBaseSchema(BaseModel):
    title: str
    description: str
    price: float
    submenu_id: uuid.UUID | None = None

    class Config:
        orm_mode = True


class CreateDishSchema(DishBaseSchema):
    pass


class DishResponse(DishBaseSchema):
    id: uuid.UUID


class UpdateDishSchema(BaseModel):
    title: str
    description: str
    price: float
    submenu_id: uuid.UUID | None = None

    class Config:
        orm_mode = True


class DishResponse4List(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    price: float


class ListDishResponse(BaseModel):
    dishes: List[DishResponse4List]

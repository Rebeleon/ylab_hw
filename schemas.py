import uuid

from pydantic import BaseModel

# from decimal import Decimal


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


class FilteredSubmenuResponse(SubmenuBaseSchema):
    id: uuid.UUID


class DishBaseSchema(BaseModel):
    title: str
    description: str
    price: str
    submenu_id: uuid.UUID | None = None

    class Config:
        orm_mode = True


class CreateDishSchema(DishBaseSchema):
    # price: Decimal
    pass


class DishResponse(DishBaseSchema):
    id: uuid.UUID


class UpdateDishSchema(DishBaseSchema):
    pass

import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import get_db


class DishRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.model = models.Dish

    async def get_all(self):
        dishes = await self.db.execute(select(models.Dish))
        dishes_response = []
        for dish in dishes.scalars():
            dishes_response.append({'id': str(dish.id), 'title': dish.title, 'description': dish.description,
                                    'price': str(dish.price)})
        return dishes_response

    async def get_by_id(self, target_dish_id: str):
        result = await self.db.execute(select(self.model).where(self.model.id == target_dish_id))
        dish = result.scalars().first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')
        return dish

    async def create(self, target_submenu_id: str, dish: schemas.CreateDishSchema):
        dish.submenu_id = uuid.UUID(target_submenu_id)
        new_dish = self.model(**dish.dict())
        self.db.add(new_dish)
        await self.db.commit()
        submenu_result = await self.db.execute(select(models.Submenu).where(models.Submenu.id == target_submenu_id))
        submenu = submenu_result.scalars().first()
        data = {'menu_id': submenu.menu_id, 'dish': new_dish}
        return data

    async def update(self, target_dish_id: str, dish: schemas.UpdateDishSchema):
        result = await self.db.execute(select(self.model).where(self.model.id == target_dish_id))
        updated_dish = result.scalars().first()
        if not updated_dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No dish with this id: {target_dish_id} found')
        dish_query = update(self.model).where(self.model.id == target_dish_id).values(
            **dish.dict(exclude_unset=True))
        await self.db.execute(dish_query)
        await self.db.commit()
        await self.db.refresh(updated_dish)
        return updated_dish

    async def delete(self, target_dish_id: str):
        result = await self.db.execute(select(models.Dish).where(models.Dish.id == target_dish_id))
        dish = result.scalars().first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No dish with this id: {target_dish_id} found')
        submenu_id = dish.submenu_id
        await self.db.delete(dish)
        await self.db.commit()
        submenu_result = await self.db.execute(select(models.Submenu).where(models.Submenu.id == submenu_id))
        submenu = submenu_result.scalars().first()
        data = {'menu_id': submenu.menu_id, 'submenu_id': submenu_id, 'dish': dish}
        return data

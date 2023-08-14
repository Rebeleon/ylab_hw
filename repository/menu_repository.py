from fastapi import Depends, HTTPException, status
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import get_db


class MenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.model = models.Menu

    async def get_all(self):
        menus = await self.db.execute(select(self.model))
        menu_response = []
        for menu in menus.scalars():
            submenus = await self.db.execute(select(models.Submenu).where(models.Submenu.menu_id == menu.id))
            dishes_count = 0
            for submenu in submenus.scalars():
                count = await self.db.execute(
                    select(func.count(models.Dish.id)).where(models.Dish.submenu_id == submenu.id))
                dishes_count += count.scalar()
            menu_response.append({'id': str(menu.id), 'title': menu.title, 'description': menu.description,
                                  'submenus_count': len(submenus.all()), 'dishes_count': dishes_count})
        return menu_response

    async def get_by_id(self, target_menu_id: str):
        result = await self.db.execute(select(self.model).where(self.model.id == target_menu_id))
        menu = result.scalars().first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        submenus = await self.db.execute(select(models.Submenu).where(models.Submenu.menu_id == menu.id))
        submenus_count = await self.db.execute(
            select(func.count(models.Submenu.id)).where(models.Submenu.menu_id == target_menu_id))
        dishes_count = 0
        for submenu in submenus.scalars():
            count = await self.db.execute(
                select(func.count(models.Dish.id)).where(models.Dish.submenu_id == submenu.id))
            dishes_count += count.scalar()
        menu_response = {'id': str(menu.id), 'title': menu.title, 'description': menu.description,
                         'submenus_count': submenus_count.scalar(), 'dishes_count': dishes_count}
        return menu_response

    async def create(self, menu: schemas.CreateMenuSchema):
        new_menu = self.model(**menu.dict())
        self.db.add(new_menu)
        await self.db.commit()
        return new_menu

    async def update(self, target_menu_id: str, menu: schemas.UpdateMenuSchema):
        result = await self.db.execute(select(self.model).where(self.model.id == target_menu_id))
        updated_menu = result.scalars().first()
        if not updated_menu:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'No menu with this id: {target_menu_id} found')
        menu_query = update(self.model).where(self.model.id == target_menu_id).values(**menu.dict(exclude_unset=True))
        await self.db.execute(menu_query)
        await self.db.commit()
        await self.db.refresh(updated_menu)
        return updated_menu

    async def delete(self, target_menu_id: str):
        result = await self.db.execute(select(self.model).where(self.model.id == target_menu_id))
        menu = result.scalars().first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No menu with this id: {target_menu_id} found')
        await self.db.delete(menu)
        await self.db.commit()
        return menu

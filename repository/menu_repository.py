from fastapi import Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import get_db

# from sqlalchemy.orm import Session


class MenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.model = models.Menu

    # def get_all(self):
    #     menus = self.db.query(models.Menu).all()
    #     menu_response = []
    #     for menu in menus:
    #         submenus = self.db.query(models.Submenu).filter(models.Submenu.menu_id == menu.id).all()
    #         dishes_count = 0
    #         for submenu in submenus:
    #             dishes_count += len(self.db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all())
    #         menu_response.append({'id': str(menu.id), 'title': menu.title, 'description': menu.description,
    #                               'submenus_count': len(submenus), 'dishes_count': dishes_count})
    #     return menu_response

    async def get_all(self):
        menus = await self.db.execute(select(models.Menu))
        menu_response = []
        for menu in menus.scalars():
            submenus = await self.db.execute(select(models.Submenu).where(models.Submenu.menu_id == menu.id))
            dishes_count = 0
            for submenu in submenus.scalars():
                dishes_count = await self.db.execute(
                    select(func.count(models.Dish.id)).where(models.Dish.submenu_id == submenu.id))
            menu_response.append({'id': str(menu.id), 'title': menu.title, 'description': menu.description,
                                  'submenus_count': len(submenus.all()), 'dishes_count': dishes_count.scalar()})
        return menu_response

    def get_by_id(self, target_menu_id: str):
        menu = self.db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                # detail=f"No menu with this id: {target_menu_id} found")
                                detail='menu not found')
        submenus = self.db.query(models.Submenu).filter(models.Submenu.menu_id == menu.id).all()
        dishes_count = 0
        for submenu in submenus:
            dishes_count += len(self.db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all())
        menu_response = {'id': str(menu.id), 'title': menu.title, 'description': menu.description,
                         'submenus_count': len(submenus), 'dishes_count': dishes_count}
        return menu_response

    def create(self, menu: schemas.CreateMenuSchema):
        new_menu = models.Menu(**menu.dict())
        self.db.add(new_menu)
        self.db.commit()
        self.db.refresh(new_menu)
        return new_menu

    def update(self, target_menu_id: str, menu: schemas.UpdateMenuSchema):
        menu_query = self.db.query(models.Menu).filter(models.Menu.id == target_menu_id)
        updated_menu = menu_query.first()
        if not updated_menu:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'No menu with this id: {target_menu_id} found')
        menu_query.update(menu.dict(exclude_unset=True), synchronize_session=False)
        self.db.commit()
        return updated_menu

    def delete(self, target_menu_id: str):
        menu_query = self.db.query(models.Menu).filter(models.Menu.id == target_menu_id)
        menu = menu_query.first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No menu with this id: {target_menu_id} found')
        menu_query.delete(synchronize_session=False)
        self.db.commit()
        return menu

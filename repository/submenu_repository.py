import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session

import models
import schemas
from database import get_db


class SubmenuRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.model = models.Submenu

    # def get_all(self):
    #     submenus = self.db.query(models.Submenu).group_by(models.Submenu.id).all()
    #     submenu_response = []
    #     for submenu in submenus:
    #         dishes = self.db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all()
    #         submenu_response.append({'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description,
    #                                  'dishes_count': len(dishes)})
    #     return submenu_response

    async def get_all(self):
        submenus = await self.db.execute(select(models.Submenu))
        submenu_response = []
        for submenu in submenus.scalars():
            dishes_count = await self.db.execute(
                select(func.count(models.Dish.id)).where(models.Dish.submenu_id == submenu.id))
            submenu_response.append({'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description,
                                     'dishes_count': dishes_count.scalar()})
        return submenu_response

    # def get_by_id(self, target_submenu_id: str):
    #     submenu = self.db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id).first()
    #     if not submenu:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail='submenu not found')
    #     dishes = self.db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all()
    #     submenu_response = {'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description,
    #                         'dishes_count': len(dishes)}
    #     return submenu_response

    async def get_by_id(self, target_submenu_id: str):
        result = await self.db.execute(select(models.Submenu).where(models.Submenu.id == target_submenu_id))
        submenu = result.scalars().first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')
        dishes_count = await self.db.execute(
            select(func.count(models.Dish.id)).where(models.Dish.submenu_id == submenu.id))
        submenu_response = ({'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description,
                             'dishes_count': dishes_count.scalar()})
        return submenu_response

    # def create(self, target_menu_id: str, submenu: schemas.CreateSubmenuSchema):
    #     submenu.menu_id = uuid.UUID(target_menu_id)
    #     new_submenu = models.Submenu(**submenu.dict())
    #     self.db.add(new_submenu)
    #     self.db.commit()
    #     self.db.refresh(new_submenu)
    #     return new_submenu

    async def create(self, target_menu_id: str, submenu: schemas.CreateSubmenuSchema):
        submenu.menu_id = uuid.UUID(target_menu_id)
        new_submenu = self.model(**submenu.dict())
        self.db.add(new_submenu)
        # await self.db.flush()
        await self.db.commit()
        return new_submenu

    # def update(self, target_submenu_id: str, submenu: schemas.UpdateSubmenuSchema):
    #     submenu_query = self.db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id)
    #     updated_submenu = submenu_query.first()
    #
    #     if not updated_submenu:
    #         raise HTTPException(status_code=status.HTTP_200_OK,
    #                             detail=f'No submenu with this id: {target_submenu_id} found')
    #     submenu_query.update(submenu.dict(exclude_unset=True), synchronize_session=False)
    #     self.db.commit()
    #     return updated_submenu

    async def update(self, target_submenu_id: str, submenu: schemas.UpdateSubmenuSchema):
        result = await self.db.execute(select(self.model).where(self.model.id == target_submenu_id))
        updated_submenu = result.scalars().first()
        if not updated_submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No submenu with this id: {target_submenu_id} found')
        submenu_query = update(self.model).where(self.model.id == target_submenu_id).values(
            **submenu.dict(exclude_unset=True))
        await self.db.execute(submenu_query)
        await self.db.commit()
        await self.db.refresh(updated_submenu)
        return updated_submenu

    # def delete(self, target_submenu_id: str):
    #     submenu_query = self.db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id)
    #     submenu = submenu_query.first()
    #     if not submenu:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                             detail=f'No submenu with this id: {target_submenu_id} found')
    #     menu_id = submenu.menu_id
    #     submenu_query.delete(synchronize_session=False)
    #     self.db.commit()
    #     data = {'menu_id': menu_id, 'submenu': submenu}
    #     return data

    async def delete(self, target_submenu_id: str):
        result = await self.db.execute(select(models.Submenu).where(models.Submenu.id == target_submenu_id))
        submenu = result.scalars().first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No submenu with this id: {target_submenu_id} found')
        menu_id = submenu.menu_id
        await self.db.delete(submenu)
        await self.db.commit()
        data = {'menu_id': menu_id, 'submenu': submenu}
        return data

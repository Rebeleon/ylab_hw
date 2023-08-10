import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db


class DishRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = models.Menu

    def get_all(self):
        dishes = self.db.query(models.Dish).group_by(models.Dish.id).all()
        dishes_response = []
        for dish in dishes:
            dishes_response.append({'id': str(dish.id), 'title': dish.title, 'description': dish.description,
                                    'price': str(dish.price)})
        return dishes_response

    def get_by_id(self, target_dish_id: str):
        dish = self.db.query(models.Dish).filter(models.Dish.id == target_dish_id).first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')
        return dish

    def create(self, target_submenu_id: str, dish: schemas.CreateDishSchema):
        dish.submenu_id = uuid.UUID(target_submenu_id)
        new_dish = models.Dish(**dish.dict())
        self.db.add(new_dish)
        self.db.commit()
        self.db.refresh(new_dish)
        menu_id = new_dish.submenu.menu_id
        data = {'menu_id': menu_id, 'dish': new_dish}
        return data

    def update(self, target_dish_id: str, dish: schemas.UpdateDishSchema):
        dish_query = self.db.query(models.Dish).filter(models.Dish.id == target_dish_id)
        updated_dish = dish_query.first()

        if not updated_dish:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'No submenu with this id: {target_dish_id} found')
        dish_query.update(dish.dict(exclude_unset=True), synchronize_session=False)
        self.db.commit()
        return updated_dish

    def delete(self, target_dish_id: str):
        dish_query = self.db.query(models.Dish).filter(models.Dish.id == target_dish_id)
        dish = dish_query.first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No dish with this id: {target_dish_id} found')
        menu_id = dish.submenu.menu_id
        submenu_id = dish.submenu_id
        dish_query.delete(synchronize_session=False)
        self.db.commit()
        data = {'menu_id': menu_id, 'submenu_id': submenu_id, 'dish': dish}
        return data

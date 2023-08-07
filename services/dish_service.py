import json
import uuid
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database import get_db
import models
import schemas

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class DishService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = models.Dish

    def get_all(self):
        key = 'dishes'
        data = r.hgetall(key)
        if data:
            dishes_list = []
            for subkey, dish in data.items():
                dish = json.loads(dish)
                dishes_list.append(dish)
            return JSONResponse(content=jsonable_encoder(dishes_list))
        dishes = self.db.query(models.Dish).group_by(models.Dish.id).all()
        dishes_response = []
        for dish in dishes:
            dishes_response.append({'id': str(dish.id), 'title': dish.title, 'description': dish.description,
                                    'price': str(dish.price)})
        for dish in dishes_response:
            subkey = f"dish:{dish['id']}"
            r.hset(key, subkey, json.dumps(dish))
        r.expire(key, time=10)
        return JSONResponse(content=jsonable_encoder(dishes_response))

    def get_by_id(self, target_dish_id: str):
        data = r.hgetall(f'get/dishes/{target_dish_id}')
        if data:
            return JSONResponse(content=jsonable_encoder(data))
        dish = self.db.query(models.Dish).filter(models.Dish.id == target_dish_id).first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='dish not found')
        dish_dict = {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}
        r.hset(f'get/dishes/{target_dish_id}', mapping=dish_dict)
        r.expire(f'get/dishes/{target_dish_id}', time=10)
        return dish

    def create(self, target_submenu_id: str, dish: schemas.CreateDishSchema):
        dish.submenu_id = uuid.UUID(target_submenu_id)
        new_dish = models.Dish(**dish.dict())
        self.db.add(new_dish)
        self.db.commit()
        self.db.refresh(new_dish)
        return new_dish

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
        dish_query.delete(synchronize_session=False)
        self.db.commit()
        return dish

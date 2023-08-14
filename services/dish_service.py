import json

import redis
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import schemas
from repository.dish_repository import DishRepository

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class DishService:
    def __init__(self, db_repository: DishRepository = Depends()):
        self.db_repository = db_repository

    async def get_all(self):
        key = 'dishes'
        data = r.hgetall(key)
        if data:
            dishes_list = []
            for subkey, dish in data.items():
                dish = json.loads(dish)
                dishes_list.append(dish)
            return JSONResponse(content=jsonable_encoder(dishes_list))

        dishes_response = await self.db_repository.get_all()

        for dish in dishes_response:
            subkey = f"dish:{dish['id']}"
            r.hset(key, subkey, json.dumps(dish))
        r.expire(key, time=10)
        return JSONResponse(content=jsonable_encoder(dishes_response))

    async def get_by_id(self, target_dish_id: str):
        data = r.hgetall(f'get/dishes/{target_dish_id}')
        if data:
            return JSONResponse(content=jsonable_encoder(data))

        dish = await self.db_repository.get_by_id(target_dish_id)

        dish_dict = {'id': str(dish.id), 'title': dish.title, 'description': dish.description, 'price': str(dish.price)}
        r.hset(f'get/dishes/{target_dish_id}', mapping=dish_dict)
        r.expire(f'get/dishes/{target_dish_id}', time=10)
        return dish

    async def create(self, target_submenu_id: str, dish: schemas.CreateDishSchema):
        data = await self.db_repository.create(target_submenu_id, dish)
        r.delete('dishes', 'submenus', 'menus', f'get/submenus/{target_submenu_id}',
                 f"get/menus/{str(data['menu_id'])}")
        return data['dish']

    async def update(self, target_dish_id: str, dish: schemas.UpdateDishSchema):
        updated_dish = await self.db_repository.update(target_dish_id, dish)
        r.delete('dishes', f'get/dishes/{target_dish_id}')
        return updated_dish

    async def delete(self, target_dish_id: str):
        data = await self.db_repository.delete(target_dish_id)
        r.delete('dishes', f'get/dishes/{target_dish_id}', 'submenus', 'menus',
                 f"get/submenus/{str(data['menu_id'])}", f"get/menus/{str(data['menu_id'])}")
        return data['dish']

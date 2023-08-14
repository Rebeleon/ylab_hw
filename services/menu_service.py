import json

import redis
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import schemas
from repository.menu_repository import MenuRepository

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class MenuService:
    def __init__(self, db_repository: MenuRepository = Depends()):
        self.db_repository = db_repository

    async def get_all(self):
        data = r.hgetall('menus')
        if data:
            menus_list = []
            for subkey, menu in data.items():
                menu = json.loads(menu)
                menus_list.append(menu)
            return JSONResponse(content=jsonable_encoder(menus_list))

        menu_response = await self.db_repository.get_all()

        key = 'menus'
        for menu in menu_response:
            subkey = f"menu:{menu['id']}"
            r.hset(key, subkey, json.dumps(menu))
        r.expire('menus', time=10)
        return JSONResponse(content=jsonable_encoder(menu_response))

    async def get_by_id(self, target_menu_id: str):
        data = r.hgetall(f'get/menus/{target_menu_id}')
        if data:
            return JSONResponse(content=jsonable_encoder(data))

        menu_response = await self.db_repository.get_by_id(target_menu_id)

        r.hset(f'get/menus/{target_menu_id}', mapping=menu_response)
        r.expire(f'get/menus/{target_menu_id}', time=10)
        return JSONResponse(content=jsonable_encoder(menu_response))

    async def create(self, menu: schemas.CreateMenuSchema):
        new_menu = await self.db_repository.create(menu)
        r.delete('menus')
        return new_menu

    async def update(self, target_menu_id: str, menu: schemas.UpdateMenuSchema):
        updated_menu = await self.db_repository.update(target_menu_id, menu)
        r.delete('menus', f'get/menus/{target_menu_id}')
        return updated_menu

    async def delete(self, target_menu_id: str):
        menu = await self.db_repository.delete(target_menu_id)
        r.delete('menus', f'get/menus/{target_menu_id}')
        return status.HTTP_200_OK

import json

import redis
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import schemas
from repository.submenu_repository import SubmenuRepository

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


class SubmenuService:
    def __init__(self, db_repository: SubmenuRepository = Depends()):
        self.db_repository = db_repository

    async def get_all(self):
        key = 'submenus'
        data = r.hgetall(key)
        if data:
            submenus_list = []
            for subkey, submenu in data.items():
                submenu = json.loads(submenu)
                submenus_list.append(submenu)
            return JSONResponse(content=jsonable_encoder(submenus_list))

        submenu_response = await self.db_repository.get_all()

        for submenu in submenu_response:
            subkey = f"menu:{submenu['id']}"
            r.hset(key, subkey, json.dumps(submenu))
        r.expire(key, time=10)
        return JSONResponse(content=jsonable_encoder(submenu_response))

    async def get_by_id(self, target_submenu_id: str):
        data = r.hgetall(f'get/submenus/{target_submenu_id}')
        if data:
            return JSONResponse(content=jsonable_encoder(data))

        submenu_response = await self.db_repository.get_by_id(target_submenu_id)

        r.hset(f'get/submenus/{target_submenu_id}', mapping=submenu_response)
        r.expire(f'get/submenus/{target_submenu_id}', time=10)
        return JSONResponse(content=jsonable_encoder(submenu_response))

    async def create(self, target_menu_id: str, submenu: schemas.CreateSubmenuSchema):
        new_submenu = await self.db_repository.create(target_menu_id, submenu)
        r.delete('submenus', 'menus', f'get/menus/{target_menu_id}')
        return new_submenu

    async def update(self, target_submenu_id: str, submenu: schemas.UpdateSubmenuSchema):
        updated_submenu = await self.db_repository.update(target_submenu_id, submenu)
        r.delete('submenus', f'get/submenus/{target_submenu_id}')
        return updated_submenu

    async def delete(self, target_submenu_id: str):
        submenu = await self.db_repository.delete(target_submenu_id)
        r.delete('submenus', f'get/submenus/{target_submenu_id}', f"get/menus/{str(submenu['menu_id'])}")
        return status.HTTP_200_OK

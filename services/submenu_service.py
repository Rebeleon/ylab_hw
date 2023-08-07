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


class SubmenuService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = models.Submenu

    def get_all(self):
        key = 'submenus'
        data = r.hgetall(key)
        if data:
            submenus_list = []
            for subkey, submenu in data.items():
                submenu = json.loads(submenu)
                submenus_list.append(submenu)
            return JSONResponse(content=jsonable_encoder(submenus_list))

        submenus = self.db.query(models.Submenu).group_by(models.Submenu.id).all()
        submenu_response = []
        for submenu in submenus:
            dishes = self.db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all()
            submenu_response.append({'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description,
                                     'dishes_count': len(dishes)})
        for submenu in submenu_response:
            subkey = f"menu:{submenu['id']}"
            r.hset(key, subkey, json.dumps(submenu))
        r.expire(key, time=10)
        return JSONResponse(content=jsonable_encoder(submenu_response))

    def get_by_id(self, target_submenu_id: str):
        data = r.hgetall(f'get/submenus/{target_submenu_id}')
        if data:
            return JSONResponse(content=jsonable_encoder(data))

        submenu = self.db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id).first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='submenu not found')
        dishes = self.db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all()
        submenu_response = {'id': str(submenu.id), 'title': submenu.title, 'description': submenu.description,
                            'dishes_count': len(dishes)}
        r.hset(f'get/submenus/{target_submenu_id}', mapping=submenu_response)
        r.expire(f'get/submenus/{target_submenu_id}', time=10)
        return JSONResponse(content=jsonable_encoder(submenu_response))

    def create(self, target_menu_id: str, submenu: schemas.CreateSubmenuSchema):
        submenu.menu_id = uuid.UUID(target_menu_id)
        new_submenu = models.Submenu(**submenu.dict())
        self.db.add(new_submenu)
        self.db.commit()
        self.db.refresh(new_submenu)
        r.delete('submenus')
        return new_submenu

    def update(self, target_submenu_id: str, submenu: schemas.UpdateSubmenuSchema):
        submenu_query = self.db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id)
        updated_submenu = submenu_query.first()

        if not updated_submenu:
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f'No submenu with this id: {target_submenu_id} found')
        submenu_query.update(submenu.dict(exclude_unset=True), synchronize_session=False)
        self.db.commit()
        r.delete('submenus', f'get/submenus/{target_submenu_id}')
        return updated_submenu

    def delete(self, target_submenu_id: str):
        submenu_query = self.db.query(models.Submenu).filter(models.Submenu.id == target_submenu_id)
        submenu = submenu_query.first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No submenu with this id: {target_submenu_id} found')
        menu_id = submenu.menu_id
        submenu_query.delete(synchronize_session=False)
        self.db.commit()
        r.delete('submenus', f'get/submenus/{target_submenu_id}', f'get/menus/{str(menu_id)}')
        return submenu


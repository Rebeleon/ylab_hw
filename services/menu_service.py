import json
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database import get_db
import models
import schemas

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


# def count_dishes_in_submenus(db, menu_id):
#     submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all()
#     dishes_count = 0
#     for submenu in submenus:
#         dishes_count += len(db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all())


class MenuService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.model = models.Menu

    def get_all(self):
        data = r.hgetall(f'menus')
        if data:
            menus_list = []
            for subkey, menu in data.items():
                menu = json.loads(menu)
                menus_list.append(menu)
            return JSONResponse(content=jsonable_encoder(menus_list))

        menus = self.db.query(models.Menu).all()
        menu_response = []
        for menu in menus:
            submenus = self.db.query(models.Submenu).filter(models.Submenu.menu_id == menu.id).all()
            dishes_count = 0
            for submenu in submenus:
                dishes_count += len(self.db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all())
            menu_response.append({'id': str(menu.id), 'title': menu.title, 'description': menu.description,
                                  'submenus_count': len(submenus), 'dishes_count': dishes_count})
        key = 'menus'
        for menu in menu_response:
            subkey = f"menu:{menu['id']}"
            r.hset(key, subkey, json.dumps(menu))
        r.expire('menus', time=10)
        return JSONResponse(content=jsonable_encoder(menu_response))

    def get_by_id(self, target_menu_id: str):
        data = r.hgetall(f'get/menus/{target_menu_id}')
        if data:
            return JSONResponse(content=jsonable_encoder(data))
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
        r.hset(f'get/menus/{target_menu_id}', mapping=menu_response)
        r.expire(f'get/menus/{target_menu_id}', time=10)
        return JSONResponse(content=jsonable_encoder(menu_response))

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



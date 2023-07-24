import schemas
import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database import get_db


router = APIRouter()


# Get menus
@router.get('/')
# @router.get('/', response_model=schemas.ListMenuResponse)
def get_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()
    menu_response = []
    for menu in menus:
        submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu.id).all()
        dishes_count = 0
        for submenu in submenus:
            dishes_count += len(db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all())
        menu_response.append({'id': menu.id, 'title': menu.title, 'description': menu.description,
                              'submenus_count': len(submenus), 'dishes_count': dishes_count})
    return JSONResponse(content=jsonable_encoder(menu_response))


# Get a single menu
@router.get('/{target_menu_id}')
def get_menu(target_menu_id: str, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            # detail=f"No menu with this id: {target_menu_id} found")
                            detail='menu not found')
    submenus = db.query(models.Submenu).filter(models.Submenu.menu_id == menu.id).all()
    dishes_count = 0
    for submenu in submenus:
        dishes_count += len(db.query(models.Dish).filter(models.Dish.submenu_id == submenu.id).all())
    menu_response = {'id': menu.id, 'title': menu.title, 'description': menu.description,
                     'submenus_count': len(submenus), 'dishes_count': dishes_count}
    return JSONResponse(content=jsonable_encoder(menu_response))


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.MenuResponse)
def create_menu(menu: schemas.CreateMenuSchema, db: Session = Depends(get_db)):
    new_menu = models.Menu(**menu.dict())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


@router.patch('/{target_menu_id}', response_model=schemas.MenuResponse)
def update_menu(target_menu_id: str, menu: schemas.UpdateMenuSchema, db: Session = Depends(get_db)):
    menu_query = db.query(models.Menu).filter(models.Menu.id == target_menu_id)
    updated_menu = menu_query.first()

    if not updated_menu:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No menu with this id: {target_menu_id} found')
    menu_query.update(menu.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_menu


@router.delete('/{target_menu_id}')
def delete_menu(target_menu_id: str, db: Session = Depends(get_db)):
    menu_query = db.query(models.Menu).filter(models.Menu.id == target_menu_id)
    menu = menu_query.first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No menu with this id: {target_menu_id} found')
    menu_query.delete(synchronize_session=False)
    db.commit()
    return menu

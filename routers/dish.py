import uuid
import schemas
import models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from decimal import Decimal
from database import get_db


router = APIRouter()


# Get dishes
@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes')
def get_dishes(db: Session = Depends(get_db)):
    dishes = db.query(models.Dish).group_by(models.Dish.id).all()
    dishes_response = []
    for dish in dishes:
        dishes_response.append({'id': dish.id, 'title': dish.title, 'description': dish.description,
                                'price': dish.price})
    return JSONResponse(content=jsonable_encoder(dishes_response))


# Get a single dish
@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.DishResponse)
def get_dish(target_dish_id: str, db: Session = Depends(get_db)):
    dish = db.query(models.Dish).filter(models.Dish.id == target_dish_id).first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='dish not found')
    return dish


@router.post('/{target_menu_id}/submenus/{target_submenu_id}/dishes', status_code=status.HTTP_201_CREATED, response_model=schemas.DishResponse)
def create_dish(target_submenu_id: str, dish: schemas.CreateDishSchema, db: Session = Depends(get_db)):
    dish.submenu_id = uuid.UUID(target_submenu_id)
    new_dish = models.Dish(**dish.dict())
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish


@router.patch('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.DishResponse)
def update_dish(target_dish_id: str, dish: schemas.UpdateDishSchema, db: Session = Depends(get_db)):
    dish_query = db.query(models.Dish).filter(models.Dish.id == target_dish_id)
    updated_dish = dish_query.first()

    if not updated_dish:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No submenu with this id: {target_dish_id} found')
    dish_query.update(dish.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return updated_dish


@router.delete('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def delete_dish(target_dish_id: str, db: Session = Depends(get_db)):
    dish_query = db.query(models.Dish).filter(models.Dish.id == target_dish_id)
    dish = dish_query.first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No dish with this id: {target_dish_id} found')
    dish_query.delete(synchronize_session=False)
    db.commit()
    return dish

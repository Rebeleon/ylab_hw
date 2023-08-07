import schemas
from fastapi import Depends, HTTPException, status, APIRouter, Response
from services.dish_service import DishService

router = APIRouter()


# Get dishes
@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes')
def get_dishes(dish: DishService = Depends()):
    return dish.get_all()


# Get a single dish
@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.DishResponse)
def get_dish(target_dish_id: str, dish: DishService = Depends()):
    return dish.get_by_id(target_dish_id)


@router.post('/{target_menu_id}/submenus/{target_submenu_id}/dishes', status_code=status.HTTP_201_CREATED, response_model=schemas.DishResponse)
def create_dish(target_submenu_id: str, dish_request: schemas.CreateDishSchema, dish: DishService = Depends()):
    return dish.create(target_submenu_id, dish_request)


@router.patch('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}', response_model=schemas.DishResponse)
def update_dish(target_dish_id: str, dish_request: schemas.UpdateDishSchema, dish: DishService = Depends()):
    return dish.update(target_dish_id, dish_request)


@router.delete('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def delete_dish(target_dish_id: str, dish: DishService = Depends()):
    return dish.delete(target_dish_id)

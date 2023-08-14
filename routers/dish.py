from fastapi import APIRouter, Depends, status

import schemas
from services.dish_service import DishService

router = APIRouter()


# Get dishes
@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes')
async def get_dishes(dish: DishService = Depends()):
    return await dish.get_all()


# Get a single dish
@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
            response_model=schemas.DishResponse)
async def get_dish(target_dish_id: str, dish: DishService = Depends()):
    return await dish.get_by_id(target_dish_id)


@router.post('/{target_menu_id}/submenus/{target_submenu_id}/dishes', status_code=status.HTTP_201_CREATED,
             response_model=schemas.DishResponse)
async def create_dish(target_submenu_id: str, dish_request: schemas.CreateDishSchema, dish: DishService = Depends()):
    return await dish.create(target_submenu_id, dish_request)


@router.patch('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}',
              response_model=schemas.DishResponse)
async def update_dish(target_dish_id: str, dish_request: schemas.UpdateDishSchema, dish: DishService = Depends()):
    return await dish.update(target_dish_id, dish_request)


@router.delete('/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
async def delete_dish(target_dish_id: str, dish: DishService = Depends()):
    return await dish.delete(target_dish_id)

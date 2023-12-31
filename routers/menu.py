from fastapi import APIRouter, Depends, status

import schemas
from services.menu_service import MenuService

# import redis

# r = redis.Redis(host='localhost', port=6379, decode_responses=True)


router = APIRouter()


# Get menus
@router.get('/')
# @router.get('/', response_model=schemas.ListMenuResponse)
async def get_menus(menu: MenuService = Depends()):
    return await menu.get_all()


# Get a single menu
@router.get('/{target_menu_id}')
async def get_menu(target_menu_id: str, menu: MenuService = Depends()):
    return await menu.get_by_id(target_menu_id)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.MenuResponse)
async def create_menu(menu_request: schemas.CreateMenuSchema, menu: MenuService = Depends()):
    return await menu.create(menu_request)


@router.patch('/{target_menu_id}', response_model=schemas.MenuResponse)
async def update_menu(target_menu_id: str, menu_request: schemas.UpdateMenuSchema, menu: MenuService = Depends()):
    return await menu.update(target_menu_id, menu_request)


@router.delete('/{target_menu_id}')
async def delete_menu(target_menu_id: str, menu: MenuService = Depends()):
    return await menu.delete(target_menu_id)

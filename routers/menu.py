import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from services.menu_service import MenuService

# import redis

# r = redis.Redis(host='localhost', port=6379, decode_responses=True)


router = APIRouter()


# Get menus
@router.get('/')
# @router.get('/', response_model=schemas.ListMenuResponse)
def get_menus(menu: MenuService = Depends()):
    return menu.get_all()


# Get a single menu
@router.get('/{target_menu_id}')
def get_menu(target_menu_id: str, menu: MenuService = Depends()):
    return menu.get_by_id(target_menu_id)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.MenuResponse)
def create_menu(menu_request: schemas.CreateMenuSchema, menu: MenuService = Depends()):
    return menu.create(menu_request)


@router.patch('/{target_menu_id}', response_model=schemas.MenuResponse)
def update_menu(target_menu_id: str, menu_request: schemas.UpdateMenuSchema, menu: MenuService = Depends()):
    return menu.update(target_menu_id, menu_request)


@router.delete('/{target_menu_id}')
def delete_menu(target_menu_id: str, menu: MenuService = Depends()):
    return menu.delete(target_menu_id)

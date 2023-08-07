import schemas
from fastapi import Depends, HTTPException, status, APIRouter
from services.submenu_service import SubmenuService


router = APIRouter()


# Get submenus
@router.get('/{target_menu_id}/submenus')
def get_submenus(submenu: SubmenuService = Depends()):
    return submenu.get_all()


# Get a single submenu
@router.get('/{target_menu_id}/submenus/{target_submenu_id}')
def get_submenu(target_submenu_id: str, submenu: SubmenuService = Depends()):
    return submenu.get_by_id(target_submenu_id)


@router.post('/{target_menu_id}/submenus', status_code=status.HTTP_201_CREATED, response_model=schemas.SubmenuResponse)
def create_submenu(target_menu_id: str, submenu_request: schemas.CreateSubmenuSchema, submenu: SubmenuService = Depends()):
    return submenu.create(target_menu_id, submenu_request)


@router.patch('/{target_menu_id}/submenus/{target_submenu_id}', response_model=schemas.MenuResponse)
def update_submenu(target_submenu_id: str, submenu_request: schemas.UpdateMenuSchema, submenu: SubmenuService = Depends()):
    return submenu.update(target_submenu_id, submenu_request)


@router.delete('/{target_menu_id}/submenus/{target_submenu_id}')
def delete_submenu(target_submenu_id: str, submenu: SubmenuService = Depends()):
    return submenu.delete(target_submenu_id)

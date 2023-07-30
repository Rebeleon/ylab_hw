from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)
ids = {}


def test_create_menu():
    response = client.post("/api/v1/menus",
                           json={
                               "title": "My menu 1",
                               "description": "My menu description 1"
                           })
    ids['menu'] = response.json()['id']


def test_create_submenu():
    response = client.post(f"/api/v1/menus/{ids['menu']}/submenus",
                           json={
                               "title": "My submenu 1",
                               "description": "My submenu description 1"
                           })
    ids['submenu'] = response.json()['id']


def test_read_dish_list():
    response = client.get(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}/dishes")
    assert response.status_code == 200
    assert response.json() == []


def test_create_dish():
    response = client.post(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}/dishes",
                           json={
                               "title": "My dish 1",
                               "description": "My dish description 1",
                               "price": "12.50"
                           })
    ids['dish'] = response.json()['id']
    assert response.status_code == 201
    assert response.json() == {
                               "id": ids['dish'],
                               "title": "My dish 1",
                               "description": "My dish description 1",
                               "price": "12.50",
                               "submenu_id": ids['submenu']
                           }


def test_read_dish():
    response = client.get(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}/dishes/{ids['dish']}")
    assert response.status_code == 200
    assert response.json() == {
                               "id": ids['dish'],
                               "title": "My dish 1",
                               "description": "My dish description 1",
                               "price": "12.50",
                               "submenu_id": ids['submenu']
                           }


def test_update_dish():
    response = client.patch(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}/dishes/{ids['dish']}",
                            json={
                                "title": "My updated dish 1",
                                "description": "My updated dish description 1",
                                "price": "14.50"
                            })
    assert response.status_code == 200
    assert response.json() == {
                               "id": ids['dish'],
                               "title": "My updated dish 1",
                               "description": "My updated dish description 1",
                               "price": "14.50",
                               "submenu_id": ids['submenu']
                          }


def test_delete_dish():
    response = client.delete(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}/dishes/{ids['dish']}")
    assert response.status_code == 200


def test_read_deleted_dish():
    response = client.get(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}/dishes/{ids['dish']}")
    assert response.status_code == 404
    assert response.json() == {"detail": "dish not found"}


def test_delete_menu():
    client.delete(f"/api/v1/menus/{ids['menu']}")

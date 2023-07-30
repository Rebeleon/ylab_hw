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


def test_create_dish():
    response = client.post(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}/dishes",
                           json={
                               "title": "My dish 1",
                               "description": "My dish description 1",
                               "price": "12.50"
                           })
    ids['dish1'] = response.json()['id']
    response = client.post(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}/dishes",
                           json={
                               "title": "My dish 2",
                               "description": "My dish description 2",
                               "price": "13.50"
                           })
    ids['dish2'] = response.json()['id']


def test_read_menu():
    response = client.get(f"/api/v1/menus/{ids['menu']}")
    assert response.status_code == 200
    assert response.json() == {
                               "id": ids['menu'],
                               "title": "My menu 1",
                               "description": "My menu description 1",
                               "submenus_count": 1,
                               "dishes_count": 2
                           }


def test_read_submenu():
    response = client.get(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}")
    assert response.status_code == 200
    assert response.json() == {
                               "id": ids['submenu'],
                               "title": "My submenu 1",
                               "description": "My submenu description 1",
                               "dishes_count": 2
                           }


def test_delete_menu():
    client.delete(f"/api/v1/menus/{ids['menu']}")

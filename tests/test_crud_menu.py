from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)
ids = {}


def test_read_menu_list():
    response = client.get("/api/v1/menus")
    assert response.status_code == 200
    assert response.json() == []


def test_create_menu():
    response = client.post("/api/v1/menus",
                           json={
                               "title": "My menu 1",
                               "description": "My menu description 1"
                           })
    ids[1] = response.json()['id']
    assert response.status_code == 201
    assert response.json() == {
                               "id": ids[1],
                               "title": "My menu 1",
                               "description": "My menu description 1"
                           }


def test_read_menu():
    response = client.get(f"/api/v1/menus/{ids[1]}")
    assert response.status_code == 200
    assert response.json() == {
                               "id": ids[1],
                               "title": "My menu 1",
                               "description": "My menu description 1",
                               "submenus_count": 0,
                               "dishes_count": 0
                           }


def test_update_menu():
    response = client.patch(f"/api/v1/menus/{ids[1]}",
                            json={
                                "title": "My updated menu 1",
                                "description": "My updated menu description 1"
                            })
    assert response.status_code == 200
    assert response.json() == {
                               "id": ids[1],
                               "title": "My updated menu 1",
                               "description": "My updated menu description 1"
                           }


def test_delete_menu():
    response = client.delete(f"/api/v1/menus/{ids[1]}")
    assert response.status_code == 200


def test_read_deleted_menu():
    response = client.get(f"/api/v1/menus/{ids[1]}")
    assert response.status_code == 404
    assert response.json() == {"detail": "menu not found"}

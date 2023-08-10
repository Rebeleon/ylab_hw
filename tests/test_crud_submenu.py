from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
ids = {}


def test_create_menu():
    response = client.post('/api/v1/menus',
                           json={
                               'title': 'My menu 1',
                               'description': 'My menu description 1'
                           })
    ids['menu'] = response.json()['id']


def test_read_submenu_list():
    response = client.get(f"/api/v1/menus/{ids['menu']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


def test_create_submenu():
    response = client.post(f"/api/v1/menus/{ids['menu']}/submenus",
                           json={
                               'title': 'My submenu 1',
                               'description': 'My submenu description 1'
                           })
    ids['submenu'] = response.json()['id']
    assert response.status_code == 201
    assert response.json() == {
        'id': ids['submenu'],
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'menu_id': ids['menu']
    }


def test_read_submenu():
    response = client.get(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}")
    assert response.status_code == 200
    assert response.json() == {
        'id': ids['submenu'],
        'title': 'My submenu 1',
        'description': 'My submenu description 1',
        'dishes_count': 0
    }


def test_update_submenu():
    response = client.patch(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}",
                            json={
                                'title': 'My updated submenu 1',
                                'description': 'My updated submenu description 1'
                            })
    assert response.status_code == 200
    assert response.json() == {
        'id': ids['submenu'],
        'title': 'My updated submenu 1',
        'description': 'My updated submenu description 1'
    }


def test_delete_submenu():
    response = client.delete(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}")
    assert response.status_code == 200


def test_read_deleted_submenu():
    response = client.get(f"/api/v1/menus/{ids['menu']}/submenus/{ids['submenu']}")
    assert response.status_code == 404
    assert response.json() == {'detail': 'submenu not found'}


def test_delete_menu():
    client.delete(f"/api/v1/menus/{ids['menu']}")

import requests
from fastapi import status


# def test_create_menu():
#     new_menu_data = {
#         "title": "Название меню",
#         "description": "Описание меню"
#     }
#     response = requests.post("http://localhost:8000/api/v1/menus", json=new_menu_data)
#     assert response.status_code == status.HTTP_201_CREATED
#     menu_info = response.json()
#     assert "id" in menu_info
#     assert menu_info["title"] == new_menu_data["title"]
#     assert menu_info["description"] == new_menu_data["description"]


def test_get_menu():
    response = requests.get("http://localhost:8000/api/v1/menus/1")
    assert response.status_code == status.HTTP_200_OK
    menu_info = response.json()
    assert "id" in menu_info
    assert "title" in menu_info
    assert "description" in menu_info


# def test_update_menu():
#     updated_menu_data = {
#         "title": "Новое название меню",
#         "description": "Новое описание меню"
#     }
#     response = requests.put("http://localhost:8000/api/v1/menus/1", json=updated_menu_data)
#     assert response.status_code == status.HTTP_200_OK
#     menu_info = response.json()
#     assert "id" in menu_info
#     assert menu_info["title"] == updated_menu_data["title"]
#     assert menu_info["description"] == updated_menu_data["description"]
#
#
# def test_delete_menu():
#     response = requests.delete("http://localhost:8000/api/v1/menus/1")
#     assert response.status_code == status.HTTP_204_NO_CONTENT

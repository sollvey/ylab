import requests
import pytest
import json
import os

from typing import Dict
from collections import defaultdict

from utils import *

app_host = os.environ["APPHOST"]
app_port = os.environ["APPPORT"]


storage = defaultdict(str)


async def get_last_row_id(table: str):
    all_rows = await get_rows(table=table)
    assert not all_rows.empty, f"Missing any rows in {table} table"
    return all_rows.sort_values("id", ascending=False).iloc[0]["id"]


async def send_request(method, path, data):
    """
    Отправка запроса
    """
    url = f"http://{app_host}:{app_port}{path_prefix}{path}"
    data = json.dumps(data)
    response = requests.request(method, url=url, data=data)
    return response


async def create_row_test(
    path: str, 
    data: Dict[str, str],
    table: str,
):
    """
    Проверка создания записи
    """
    prev_number = len(await get_rows(table))
    res = await send_request(method="POST", path=path, data=data)
    res_data = res.json()
    assert res.status_code == 201, "Status code error"
    next_number = len(await get_rows(table))
    assert prev_number + 1 == next_number, "Length error"
    for column, value in data.items():
        assert res_data[column] == value, f"Column {column} error"
    storage[f"test_{table}_id"] = res_data["id"]


async def get_rows_test(path: str):
    """
    Проверка получения списка записей
    """
    res = await send_request(method="GET", path=path, data=None)
    assert res.status_code == 200, "Status code error"


async def update_row_test(
    path: str,
    data: Dict[str, str],
    table: str,
    conditions: Dict[str, Union[int, str]],
):
    """
    Проверка изменения записи
    """
    prev_data = await get_rows(
        table=table,
        conditions=conditions,
    )
    assert not prev_data.empty, f"Missing row in {table} table"
    prev_data = prev_data.to_dict(orient="records")[0]
    res = await send_request(method="PATCH", path=path, data=data)
    res_data = res.json()
    assert res.status_code == 200, "Status code error"
    for column, value in data.items():
        assert res_data[column] == value, f"Column {column} error"
        assert res_data[column] != prev_data[column], f"Column {column} error"


async def delete_row_test(
    path: str,
    table: str,
    conditions: Dict[str, Union[int, str]],
):
    """
    Проверка удаления записи
    """
    prev_data = await get_rows(
        table=table,
        conditions=conditions,
    )
    assert not prev_data.empty, f"Missing row in {table} table"
    prev_data = prev_data.to_dict(orient="records")[0]
    res = await send_request(method="DELETE", path=path, data=None)
    assert res.status_code == 200, "Status code error"
    curr_data = await get_rows(
        table=table,
        conditions=conditions,
    )
    assert curr_data.empty, "Row wasn't delete"


@pytest.mark.asyncio
@pytest.mark.base
async def test_create_menu():
    await create_row_test(
        path="/menus",
        data={"title": "My menu", "description": "My menu description"},
        table="menu"
    )
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_create_submenu():
    last_menu_id = storage.get("test_menu_id")
    await create_row_test(
        path=f"/menus/{last_menu_id}/submenus",
        data={"title": "My submenu", "description": "My submenu description"},
        table="submenu"
    )
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_create_dish():
    last_menu_id = storage.get("test_menu_id")
    last_submenu_id = storage.get("test_submenu_id")
    await create_row_test(
        path=f"/menus/{last_menu_id}/submenus/{last_submenu_id}/dishes",
        data={"title": "My dish", "description": "My dish description", "price": "12.50"},
        table="dish"
    )
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_get_menus():
    await get_rows_test(path="/menus")
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_get_submenus():
    last_menu_id = storage.get("test_menu_id")
    await get_rows_test(path=f"/menus/{last_menu_id}/submenus")
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_get_dishes():
    last_menu_id = storage.get("test_menu_id")
    last_submenu_id = storage.get("test_submenu_id")
    await get_rows_test(path=f"/menus/{last_menu_id}/submenus/{last_submenu_id}/dishes")
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_get_menu():
    last_menu_id = storage.get("test_menu_id")
    await get_rows_test(path=f"/menus/{last_menu_id}")
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_get_submenu():
    last_menu_id = storage.get("test_menu_id")
    last_submenu_id = storage.get("test_submenu_id")
    await get_rows_test(path=f"/menus/{last_menu_id}/submenus/{last_submenu_id}")
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_get_dish():
    last_menu_id = storage.get("test_menu_id")
    last_submenu_id = storage.get("test_submenu_id")
    last_dish_id = storage.get("test_dish_id")
    await get_rows_test(path=f"/menus/{last_menu_id}/submenus/{last_submenu_id}/dishes/{last_dish_id}")
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_update_menu():
    last_menu_id = storage.get("test_menu_id")
    await update_row_test(
        path=f"/menus/{last_menu_id}",
        data={"title": "My upd menu", "description": "My upd description menu"},
        table="menu",
        conditions={"id": last_menu_id}
    )
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_update_submenu():
    last_menu_id = storage.get("test_menu_id")
    last_submenu_id = storage.get("test_submenu_id")
    await update_row_test(
        path=f"/menus/{last_menu_id}/submenus/{last_submenu_id}",
        data={"title": "My upd submenu", "description": "My upd description submenu"},
        table="submenu",
        conditions={"id": last_submenu_id, "menu_id": last_menu_id}
    )
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_update_dish():
    last_menu_id = storage.get("test_menu_id")
    last_submenu_id = storage.get("test_submenu_id")
    last_dish_id = storage.get("test_dish_id")
    await update_row_test(
        path=f"/menus/{last_menu_id}/submenus/{last_submenu_id}/dishes/{last_dish_id}",
        data={"title": "My upd dish", "description": "My upd description dish", "price": "14.50"},
        table="dish",
        conditions={"id": last_dish_id, "submenu_id": last_submenu_id}
    )
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_delete_dish():
    last_menu_id = storage.get("test_menu_id")
    last_submenu_id = storage.get("test_submenu_id")
    last_dish_id = storage.get("test_dish_id")
    await delete_row_test(
        path=f"/menus/{last_menu_id}/submenus/{last_submenu_id}/dishes/{last_dish_id}",
        table="dish",
        conditions={"id": last_dish_id, "submenu_id": last_submenu_id}
    )
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_delete_submenu():
    last_menu_id = storage.get("test_menu_id")
    last_submenu_id = storage.get("test_submenu_id")
    await delete_row_test(
        path=f"/menus/{last_menu_id}/submenus/{last_submenu_id}",
        table="submenu",
        conditions={"id": last_submenu_id, "menu_id": last_menu_id}
    )
    return True


@pytest.mark.asyncio
@pytest.mark.base
async def test_delete_menu():
    last_menu_id = storage.get("test_menu_id")
    await delete_row_test(
        path=f"/menus/{last_menu_id}",
        table="menu",
        conditions={"id": last_menu_id}
    )
    return True
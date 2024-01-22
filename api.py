from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from schemas import *
from utils import *

menu_v1_router = APIRouter(prefix="/api/v1")

######################
######## MENU ########
######################

@menu_v1_router.post("/menus", tags=["menu"])
async def create_menu(data: MainFieldsPy) -> JSONResponse:
    """
    Создание нового меню
    """
    try:
        await create_row(
            data=dict(data),
            table="menu",
        )
        return JSONResponse({"message": "Меню создано"}, status_code=201)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.get("/menus", tags=["menu"])
async def menu_list() -> List[GetMenuPy]:
    """
    Получение списка меню
    """
    try:
        menus = await get_rows(table="menu")
        if menus.empty:
            return []
        return [GetMenuPy(**row) for row in menus.to_dict(orient="records")]
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)


@menu_v1_router.get("/menus/{menu_id}", tags=["menu"])
async def menu(menu_id: int) -> GetMenuPy:
    """
    Получение меню
    """
    try:
        menu = await get_rows(
            table="menu",
            conditions={"id": menu_id},
        )
        if menu.empty:
            return JSONResponse(
                {"message": "menu not found", "content": []},
                status_code=404,
            )
        menu = menu.to_dict(orient="records")[0]
        menu["title"] = None
        menu["description"] = None
        return GetMenuPy(**menu)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.patch("/menus/{menu_id}", tags=["menu"])
async def update_menu(menu_id: int, data: MainFieldsPy) -> JSONResponse:
    """
    Обновление меню
    """
    try:
        await update_row(
            data=dict(data),
            table="menu",
            conditions={"id": menu_id},
        )
        return JSONResponse({"message": "Меню обновлено"}, status_code=200)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)


@menu_v1_router.delete("/menus/{menu_id}", tags=["menu"])
async def delete_menu(menu_id: int) -> JSONResponse:
    """
    Удаление меню
    """
    try:
        await delete_row(
            table="menu",
            conditions={"id": menu_id},
        )
        return JSONResponse({"message": "Меню удалено"}, status_code=200)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)


#########################
######## SUBMENU ########
#########################

@menu_v1_router.post("/menus/{menu_id}/submenus", tags=["menu"])
async def create_submenu(menu_id: int, data: MainFieldsPy) -> JSONResponse:
    """
    Создание нового подменю
    """
    try:
        await create_row(
            data=dict(data) | {"menu_id": menu_id},
            table="submenu",
        )
        return JSONResponse({"message": "Подменю создано"}, status_code=201)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.get("/menus/{menu_id}/submenus", tags=["submenu"])
async def submenu_list() -> List[GetSubmenuPy]:
    """
    Получение списка подменю
    """
    try:
        submenus = await get_rows(table="submenu")
        if submenus.empty:
            return []
        return [GetSubmenuPy(**row) for row in submenus.to_dict(orient="records")]
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)


@menu_v1_router.get("/menus/{menu_id}/submenus/{submenu_id}", tags=["submenu"])
async def submenu(menu_id: int, submenu_id: int) -> GetSubmenuPy:
    """
    Получение подменю
    """
    try:
        submenu = await get_rows(
            table="submenu",
            conditions={"id": submenu_id, "menu_id": menu_id},
        )
        if submenu.empty:
            return JSONResponse(
                {"message": "submenu not found", "content": []},
                status_code=404,
            )
        submenu = submenu.to_dict(orient="records")[0]
        submenu["title"] = None
        submenu["description"] = None
        return GetSubmenuPy(**submenu)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.patch("/menus/{menu_id}/submenus/{submenu_id}", tags=["submenu"])
async def update_submenu(menu_id: int, submenu_id: int, data: MainFieldsPy) -> JSONResponse:
    """
    Обновление подменю
    """
    try:
        await update_row(
            data=dict(data),
            table="submenu",
            conditions={"id": submenu_id, "menu_id": menu_id},
        )
        return JSONResponse({"message": "Подменю обновлено"}, status_code=200)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)


@menu_v1_router.delete("/menus/{menu_id}/submenus/{submenu_id}", tags=["submenu"])
async def delete_menu(menu_id: int, submenu_id: int) -> JSONResponse:
    """
    Удаление подменю
    """
    try:
        await delete_row(
            table="submenu",
            conditions={"id": submenu_id, "menu_id": menu_id},
        )
        return JSONResponse({"message": "Подменю удалено"}, status_code=200)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    


######################
######## DISH ########
######################

@menu_v1_router.post("/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["dish"])
async def create_dish(menu_id: int, submenu_id: int, data: MainDishPy) -> JSONResponse:
    """
    Создание нового блюда
    """
    try:
        data = dict(data)
        if isinstance(data["price"], str):
            data["price"] = float(data["price"])
        await create_row(
            data=data | {"submenu_id": submenu_id},
            table="dish",
        )
        return JSONResponse({"message": "Блюдо создано"}, status_code=201)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["dish"])
async def dish_list() -> List[GetDishPy]:
    """
    Получение списка блюд
    """
    try:
        dishes = await get_rows(table="dish")
        if dishes.empty:
            return []
        return [GetDishPy(**row) for row in dishes.to_dict(orient="records")]
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)


@menu_v1_router.get("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["dish"])
async def dish(menu_id: int, submenu_id: int, dish_id: int) -> GetDishPy:
    """
    Получение блюда
    """
    try:
        dish = await get_rows(
            table="dish",
            conditions={"id": dish_id, "submenu_id": submenu_id},
        )
        if dish.empty:
            return JSONResponse(
                {"message": "dish not found", "content": []},
                status_code=404,
            )
        dish = dish.to_dict(orient="records")[0]
        dish["title"] = None
        dish["description"] = None
        return GetDishPy(**dish)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["dish"])
async def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    data: MainFieldsPy
) -> JSONResponse:
    """
    Обновление блюда
    """
    try:
        await update_row(
            data=dict(data) | {"submenu_id": submenu_id},
            table="dish",
            conditions={"id": dish_id, "submenu_id": submenu_id},
        )
        return JSONResponse({"message": "Блюдо обновлено"}, status_code=200)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)


@menu_v1_router.delete("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["dish"])
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int) -> JSONResponse:
    """
    Удаление блюда
    """
    try:
        await delete_row(
            table="dish",
            conditions={"id": dish_id, "submenu_id": submenu_id},
        )
        return JSONResponse({"message": "Блюдо удалено"}, status_code=200)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
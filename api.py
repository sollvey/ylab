from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from schemas import *
from utils import *
from models import *

menu_v1_router = APIRouter(prefix=path_prefix)

######################
######## MENU ########
######################

@menu_v1_router.post("/menus", tags=["menu"])
async def create_menu(data: MainFieldsPy) -> JSONResponse:
    """
    Создание нового меню
    """
    try:
        data = dict(data)
        menu_id = await create_row(data=data, table="menu")
        return JSONResponse(
            {"id": str(menu_id)} | data,
            status_code=201
        )
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
async def menu(menu_id: int) -> GetCountMenuPy:
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
                {"message": "menu not found", "detail": "menu not found"},
                status_code=404,
            )
        menu = menu.to_dict(orient="records")[0]
        with get_session() as session:
            submenus = session.query(SubmenuPy).filter(
                SubmenuPy.menu_id == menu_id
            ).all()
            submenus_ids = [subm.id for subm in submenus]
            if submenus_ids:
                dishes = session.query(DishPy).filter(
                    DishPy.submenu_id.in_(submenus_ids)
                ).join(
                    SubmenuPy, DishPy.submenu_id == SubmenuPy.id
                ).filter(
                    SubmenuPy.menu_id == menu_id
                ).all()
            else:
                dishes = []
        menu["id"] = str(menu["id"])
        menu["submenus_count"] = len(submenus)
        menu["dishes_count"] = len(dishes)
        return GetCountMenuPy(**menu)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.patch("/menus/{menu_id}", tags=["menu"])
async def update_menu(menu_id: int, data: MainFieldsPy) -> JSONResponse:
    """
    Обновление меню
    """
    try:
        data = dict(data)
        await update_row(
            data=data,
            table="menu",
            conditions={"id": menu_id},
        )
        return JSONResponse(data, status_code=200)
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

@menu_v1_router.post("/menus/{menu_id}/submenus", tags=["submenu"])
async def create_submenu(menu_id: int, data: MainFieldsPy) -> JSONResponse:
    """
    Создание нового подменю
    """
    try:
        data = dict(data)
        submenu_id = await create_row(
            data=data | {"menu_id": menu_id},
            table="submenu",
        )
        return JSONResponse(
            {"id": str(submenu_id)} | data,
            status_code=201
        )
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
async def submenu(menu_id: int, submenu_id: int) -> GetCountSubmenuPy:
    """
    Получение подменю
    """
    try:
        submenu = await get_rows(
            table="submenu",
            conditions={"menu_id": menu_id, "id": submenu_id},
        )
        if submenu.empty:
            return JSONResponse(
                {"message": "submenu not found", "detail": "submenu not found"},
                status_code=404,
            )
        submenu = submenu.to_dict(orient="records")[0]
        with get_session() as session:
            dishes = session.query(DishPy).filter(
                DishPy.submenu_id == submenu_id
            ).join(
                SubmenuPy, DishPy.submenu_id == SubmenuPy.id
            ).filter(
                SubmenuPy.menu_id == menu_id
            ).all()
        submenu["id"] = str(submenu["id"])
        submenu["dishes_count"] = len(dishes)
        return GetCountSubmenuPy(**submenu)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.patch("/menus/{menu_id}/submenus/{submenu_id}", tags=["submenu"])
async def update_submenu(menu_id: int, submenu_id: int, data: MainFieldsPy) -> JSONResponse:
    """
    Обновление подменю
    """
    try:
        data = dict(data)
        await update_row(
            data=data,
            table="submenu",
            conditions={"id": submenu_id, "menu_id": menu_id},
        )
        return JSONResponse(data, status_code=200)
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
        dish_id = await create_row(
            data=data | {"submenu_id": submenu_id},
            table="dish",
        )
        data["price"] = f"{data['price']:.2f}"
        return JSONResponse(
            {"id": str(dish_id)} | data,
            status_code=201
        )
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
                {"message": "dish not found", "detail": "dish not found"},
                status_code=404,
            )
        dish = dish.to_dict(orient="records")[0]
        dish["id"] = str(dish["id"])
        dish["price"] = f"{dish['price']:.2f}"
        return GetDishPy(**dish)
    except Exception as exception:
        return JSONResponse({"message": exception}, status_code=400)
    

@menu_v1_router.patch("/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", tags=["dish"])
async def update_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    data: MainDishPy
) -> JSONResponse:
    """
    Обновление блюда
    """
    try:
        data = dict(data)
        await update_row(
            data=data | {"submenu_id": submenu_id},
            table="dish",
            conditions={"id": dish_id, "submenu_id": submenu_id},
        )
        return JSONResponse(data, status_code=200)
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

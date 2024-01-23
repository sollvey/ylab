from pydantic import BaseModel
from typing import Union


class MainFieldsPy(BaseModel):
    title: str
    description: str


class GetMenuPy(MainFieldsPy):
    id: Union[int, str]


class GetCountMenuPy(GetMenuPy):
    submenus_count: Union[int, str]
    dishes_count: Union[int, str]


class GetSubmenuPy(MainFieldsPy):
    id: Union[int, str]
    menu_id: Union[int, str]


class GetCountSubmenuPy(GetSubmenuPy):
    dishes_count: Union[int, str]


class MainDishPy(MainFieldsPy):
    price: Union[str, float]


class GetDishPy(MainDishPy):
    id: Union[int, str]
    submenu_id: Union[int, str]
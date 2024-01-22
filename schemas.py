from pydantic import BaseModel
from typing import Union

class MainFieldsPy(BaseModel):
    title: Union[str, None]
    description: Union[str, None]


class GetMenuPy(MainFieldsPy):
    id: int


class GetSubmenuPy(BaseModel):
    id: int
    menu_id: int


class MainDishPy(MainFieldsPy):
    price: Union[str, float]


class GetDishPy(BaseModel):
    id: int
    submenu_id: int
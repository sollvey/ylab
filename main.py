from fastapi import FastAPI

from api import menu_v1_router

app = FastAPI()
app.include_router(menu_v1_router)
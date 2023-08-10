from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from routers import dish, menu, submenu

# from redis import asyncio as aioredis
# import redis


app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(menu.router, tags=['Menus'], prefix='/api/v1/menus')
app.include_router(submenu.router, tags=['Submenus'], prefix='/api/v1/menus')
app.include_router(dish.router, tags=['Dishes'], prefix='/api/v1/menus')


# @app.on_event("startup")
# async def startup():
# redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
# FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache", key_builder=request_key_builder)


@app.get('/api/healthchecker')
def root():
    message = [{'message': 'Hello World'}]
    return JSONResponse(content=jsonable_encoder(message))

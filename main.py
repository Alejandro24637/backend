from fastapi import FastAPI
from routers import products,users,basic_user_oath2,jwt_user_oauth2,users_db
from fastapi.staticfiles import StaticFiles

# documentacion de FastApi https://fastapi.tiangolo.com/es/tutorial/first-steps/


# instanciamos a FastApi
app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_user_oath2.router)
app.include_router(jwt_user_oauth2.router)
app.include_router(users_db.router)
# Recurso estatico
app.mount("/static", StaticFiles(directory="static"), name="static")


# iniciar servidor local: uvicorn main:app --reload
# Hacemos un Hola mundo con una peticion http 'get' y un decorador de @app a una funcion asincrona

# url http://127.0.0.1:8000

@app.get("/")
async def root():
    return {"message": "OLAAAAAA YAYAJUUUUU"}

# url http://127.0.0.1:8000/video

@app.get("/video")
async def url():
    return {"url_canciones": "https://www.youtube.com/watch?v=khMb3k-Wwvg&list=PLCkMH7xAN6uyvIupkJb33DYK6h4QcZ7ET&index=12"}


# documentacion automatica con Swagger '/docs'
# documentacion automatica con Redoc '/redoc'
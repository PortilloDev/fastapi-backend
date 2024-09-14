from fastapi import FastAPI
from routers.book_routes import router as book_router
from routers.user_routes import router as user_router
from routers.basic_auth_user_router import router as auth_router
from routers.jwt_auth_users_router import router as jwt_auth_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
# Iniciar el servidor  uvicorn main:app --reload


app.include_router(book_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(jwt_auth_router)

## A partir de está configuración, podemos acceder a los archivos estáticos en la ruta /static
## solo debemos agregar la ruta de la imagen en la url
## http://127.0.0.1:8000/static/images/424606503_360442953561893_1504963896564635832_n.jpg
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Welcome to the API Bookstore"}


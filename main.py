from fastapi import FastAPI
from api.book_routes import router as book_router
from api.user_routes import router as user_router

app = FastAPI()
# Iniciar el servidor  uvicorn main:app --reload


app.include_router(book_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API Bookstore"}


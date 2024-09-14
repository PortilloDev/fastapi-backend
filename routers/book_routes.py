# api/book_routes.py
from fastapi import APIRouter, HTTPException
from models.book import Book
from repositories.book_repository import BookRepository

router = APIRouter(
    prefix="/api/v1/books",
    tags=["Books"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def get_books():
    return BookRepository.get_all_books()

@router.get("/{book_id}")
async def get_book(book_id: int):
    book = BookRepository.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/")
async def create_book(book: Book):
    BookRepository.add_book(book)
    return {"id": book.id}

@router.delete("/{book_id}")
async def delete_book(book_id: int):
    book = BookRepository.delete_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}

# api/book_routes.py
from fastapi import APIRouter, HTTPException
from models.book import Book
from repositories.book_repository import BookRepository

router = APIRouter()

@router.get("/api/v1/books/")
async def get_books():
    return BookRepository.get_all_books()

@router.get("/api/v1/books/{book_id}")
async def get_book(book_id: int):
    book = BookRepository.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/api/v1/books/")
async def create_book(book: Book):
    BookRepository.add_book(book)
    return {"id": book.id}

@router.delete("/api/v1/books/{book_id}")
async def delete_book(book_id: int):
    book = BookRepository.delete_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}

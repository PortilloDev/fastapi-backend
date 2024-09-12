# repositories/book_repository.py
from models.book import Book

books_list = []

class BookRepository:

    @staticmethod
    def get_all_books():
        return books_list

    @staticmethod
    def get_book_by_id(book_id: int):
        book = filter(lambda b: b.id == book_id, books_list)
        try:
            return list(book)[0]
        except IndexError:
            return None

    @staticmethod
    def add_book(book: Book):
        books_list.append(book)
        return book

    @staticmethod
    def delete_book(book_id: int):
        book = BookRepository.get_book_by_id(book_id)
        if book:
            books_list.remove(book)
        return book

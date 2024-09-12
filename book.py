
@app.get("/login")
async def login():
    return {"message":  "Login" }


@app.get("/api/v1/books/")
async def books():
    return books_list


@app.get("/api/v1/books/{book_id}")
async def book(book_id: int):
    return search_book(book_id)



@app.get("/api/v1/books-query/")
async def book(book_id: int):
    return search_book(book_id)
    

@app.post("/api/v1/books/")
async def create_book(book: Book):
    #id = len(books_list) + 1
    Book(id=book.id, title=book.title, description=book.description, pages=book.pages, authors=book.authors)
    books_list.append(book)
    return book.id


@app.delete("/api/v1/books/{book_id}")
async def delete_book(book_id: int):
    book = search_book(book_id)
    books_list.remove(book)
    return {"message": "Book deleted"}

    
    
def search_book(book_id: int):
    book = filter(lambda book: book.id == book_id, books_list)
    try:
        return list(book)[0]
    except:
        return {"error": "Book not found"}
from library import Library
from models import Book, Member

def main():
    library = Library()
    library.add_book(Book("978-1", "Clean Code"))
    library.register(Member("m1", "Alice"))
    library.borrow("978-1", "m1")
    print("After borrowing: ", library.snapshot())
    library.return_book("978-1")
    print("Available: ", [book.title for book in library.available_books()])

if __name__ == "__main__":
    main()
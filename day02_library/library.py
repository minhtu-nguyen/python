from dataclasses import asdict
from models import Book, Member

class Library:
    def __init__(self):
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        self.loans: dict[str, str] = {} # isbn -> member_id

    def add_book(self, book: Book):
        if book.isbn in self.books:
            raise ValueError("Book already exists")
        self.books[book.isbn] = book

    def register(self, member: Member):
        if member.member_id in self.members:
            raise ValueError("Member already exists")
        self.members[member.member_id] = member

    def borrow(self, isbn: str, member_id: str):
        if isbn not in self.books:
            raise ValueError("Unknown book")
        if member_id not in self.members:
            raise ValueError("Unknown member")
        if not self.books[isbn].available:
            raise ValueError("Booko is already borrowed")
        self.books[isbn].available = False
        self.loans[isbn] = member_id

    def return_book(self, isbn: str):
        if isbn not in self.loans:
            raise ValueError("Book is not borrowed")
        del self.loans[isbn]
        self.books[isbn].available = True

    def available_books(self) -> list[Book]:
        return [book for book in self.books.values() if book.available]

    def snapshot(self) -> dict:
        return {
            "books": [asdict(book) for book in self.books.values()],
            "members": [asdict(member) for member in self.members.values()],
            "loans": self.loans.copy()
        }
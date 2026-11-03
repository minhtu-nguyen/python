import json
from pathlib import Path
from library import Library
from models import Book, Member

def save_library(library: Library, path: Path):
    path.write_text(json.dumps(library.snapshot(), indent=2), encoding="utf-8")

def load_library(path: Path) -> Library:
    data = json.loads(path.read_text(encoding="utf-8"))
    library = Library()
    for row in data["books"]:
        library.add_book(Book(**row))
    for row in data["members"]:
        library.register(Member(**row))
    library.loans = dict(data["loans"])
    if any(isbn not in library.books or member not in library.members for isbn, member in library.loans.items()):
        raise ValueError("Invalid loan references")
    if any(book.available == (isbn in library.loans) for isbn, book in library.books.items()):
        raise ValueError("Inconsistent book availability")
    return library
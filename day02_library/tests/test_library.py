import pytest
from library import Library
from models import Book, Member
from persistence import save_library, load_library

def test_borrow_return_and_persistence(tmp_path):
    library = Library()
    library.add_book(Book("1", "Python"))
    library.register(Member("m1", "Alice"))
    library.borrow("1", "m1")
    with pytest.raises(ValueError, match="already borrowed"):
        library.borrow("1", "m1")
    path = tmp_path / "library.json"
    save_library(library, path)
    restored = load_library(path)
    assert not restored.books["1"].available
    restored.return_book("1")
    assert restored.books["1"].available
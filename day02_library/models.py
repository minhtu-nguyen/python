from dataclasses import dataclass

@dataclass
class Book:
    isbn: str
    title: str
    available: bool = True

    def __post_init__(self):
        if not self.isbn.strip() or not self.title.strip():
            raise ValueError("ISBN and title are required")

@dataclass
class Member:
    member_id: str
    name: str

    def __post_init__(self):
        if not self.member_id.strip() or not self.name.strip():
            raise ValueError("Member ID and name are required")

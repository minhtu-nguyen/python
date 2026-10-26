# 7-Day Python: Detailed Professional Hands-on Walkthrough (Days 1–7)

**Duration:** 7 days · **Time:** 4–6 hours/day · **Goal:** Build seven small projects using real development practices.

> This is an intensive review and introduction to advanced practices, not a guarantee of mastery in one week. All commits below are commands **you run**; they are not claims that commits were made in your repository.

## Roadmap

| Day | Focus | Project |
|---|---|---|
| 1 | Functions, validation, JSON, CLI | Expense Tracker |
| 2 | OOP, dataclasses, composition | Library Management |
| 3 | Generators, decorators, streaming | Log Analyzer |
| 4 | Algorithms and `asyncio` | Async API Aggregator |
| 5 | SQL, FastAPI, CRUD | Task Manager API |
| 6 | Testing, mocking, linting, CI | Hardened Task Manager |
| 7 | Integration and architecture | Job Application Tracker API |

## Before you start

## How to read this guide

Each step now includes a **Why this design?** section. Treat these as engineering trade-offs, not rules that apply to every project. Before copying code, predict what it will do; afterward, run the supplied command, inspect the result, and make the indicated commit. A successful test run proves only the cases that were tested.

**Why commit in small increments?** Small, logically focused commits are easier to review, revert, and debug. Read the staged diff (`git diff --cached`) before each commit, so unintended files do not sneak in.


Install Python 3.11+ and Git. Commands use macOS/Linux shells; on Windows use PowerShell equivalents for activation and creating files. All code blocks labeled with a filename should be saved to that filename.

```bash
mkdir python-7-day-challenge && cd python-7-day-challenge
git init
git branch -M main
python -m venv .venv
source .venv/bin/activate   # PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pytest "fastapi[standard]" httpx ruff
printf '.venv/\n__pycache__/\n.pytest_cache/\n.ruff_cache/\n*.pyc\n*.db\n*.json.tmp\n' > .gitignore
printf '# Python 7-Day Challenge\n\nSeven projects and incremental Git commits.\n' > README.md
git add .gitignore README.md
git diff --cached
git commit -m "chore: initialize seven-day Python workspace"
```

**Professional rule for every change:** edit → run/check → `git status` → `git diff` → `git add <specific files>` → `git diff --cached` → `git commit -m "type: message"`. Do not commit `.venv`, secrets, generated databases, or personal data.

---

# Day 1 — Expense Tracker CLI

## Your mission and definition of done

**End product:** A clean, testable command-line program.

**Core review concepts:** Parsing string input; precise money; JSON; list and dictionary processing; command-line flags.

**Definition of done:** You should be able to explain the flow `CLI → validation → storage → reporting`, reproduce one invalid input, and restore your data after restarting the CLI.

**Scope boundary:** The entire app runs locally; do not commit the personal `expenses.json` file.

### How to approach every step

1. Read the rationale before opening the editor. Predict the shape of the input and output.
2. Create the named file exactly where the guide says, and enter the full code block.
3. Execute the smoke-test command, then deliberately try one invalid input.
4. Run tests where available, inspect `git status` and `git diff --cached`, and commit only the milestone's files.
5. Write down one design trade-off you would discuss during a code review.

**Commit convention:** `feat` for behavior, `test` for tests, `refactor` for restructuring without changed behavior, `docs` for documentation, and `chore` for tooling and setup. Hashes on your machine will naturally differ from another repository's.


**Learn:** types, functions, dictionaries, exceptions, `Decimal`, JSON, CSV, CLI arguments, unit tests.

## Step 1. Define and validate an expense

**Why store `amount_cents` as an integer rather than `12.50` as a float?** Binary floating-point cannot exactly represent many decimal fractions: in Python, `0.1 + 0.2` is not exactly `0.3`. Parse user input with `Decimal` and convert to whole cents so additions and comparisons are exact for this application's two-decimal currency model. This assumes one currency with two minor-unit digits; international or multi-currency systems need explicit currency metadata and may use `Decimal` throughout.

**Why validate at the boundary?** Reject bad amounts, blank categories, and invalid dates before they enter the application. Normalizing category names makes `" FOOD "` and `"food"` aggregate together. A dictionary keeps Day 1 approachable; Day 2 introduces stronger domain models.


```bash
mkdir -p day01_expenses/tests
cd day01_expenses
```

**Read this file like a reviewer — `day01_expenses/expense.py`:** Read the public interface first; inspect error paths before the happy path. Keep it in a separate editor tab as you run the example.

**`day01_expenses/expense.py`**

```python
from datetime import date
from decimal import Decimal, InvalidOperation


def to_cents(text: str) -> int:
    try:
        amount = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError("Amount must be numeric") from exc
    if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
        raise ValueError("Amount must be positive with at most 2 decimal places")
    return int(amount * 100)


def make_expense(amount: str, category: str, note: str = "", when: str | None = None) -> dict:
    category = category.strip().lower()
    if not category:
        raise ValueError("Category is required")
    day = date.fromisoformat(when) if when else date.today()
    return {"date": day.isoformat(), "category": category,
            "amount_cents": to_cents(amount), "note": note.strip()}
```

**Try it:**

```bash
python -c 'from expense import make_expense; print(make_expense("12.50", " FOOD ", "lunch", "2026-10-21"))'
git add expense.py && git diff --cached
git commit -m "feat(day1): validate expense records and store integer cents"
```


### Checkpoint — What to inspect

**Run and inspect:** Validate three cases: `"5.25"` should become 525 cents, `"0"` should be rejected, and a blank category should be rejected. Use `python -c` or the REPL. Why: demonstration of a successful path alone misses important boundary behavior.

**Code-review discussion:** Predict whether the function mutates an existing dictionary or constructs a new one. Prefer returning a new record so calling code controls when to persist it.

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 2. Add JSON persistence and reports

**Why use a temporary file?** Rewriting the live JSON file directly can leave it truncated if a process fails midway. Here we write complete JSON to a temporary sibling and then replace the destination, greatly reducing the chance of partial output. `Path.replace` is commonly atomic when both paths are on the same local filesystem, but it is **not** a backup, a durability guarantee after power loss, or safe for simultaneous writers. This example uses a predictable `.tmp` filename, so concurrent saves can conflict; a production app should use uniquely named temporary files, locking, or a database.

**Why isolate storage from reporting?** `storage.py` owns file operations, while `reports.py` owns transformation and presentation data. This separation lets you test spending calculations without touching disk, and later replace JSON with a database without rewriting reporting logic.

**Why `newline=""` for CSV?** The Python `csv` module handles newline conventions itself; this setting avoids extra blank lines on some platforms. **Why `defaultdict(int)`?** It creates a zero total for each new category without repetitive membership checks.


**Read this file like a reviewer — `day01_expenses/storage.py`:** Read the public interface first; inspect error paths before the happy path. Keep it in a separate editor tab as you run the example.

**`day01_expenses/storage.py`**

```python
import json
from pathlib import Path


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Expense file must contain a JSON list")
    return data


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
```

**Read this file like a reviewer — `day01_expenses/reports.py`:** Read the public interface first; inspect error paths before the happy path. Keep it in a separate editor tab as you run the example.

**`day01_expenses/reports.py`**

```python
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path


def by_month(rows: list[dict], month: str | None) -> list[dict]:
    if month is None:
        return rows
    if len(month) != 7:
        raise ValueError("Month must be YYYY-MM")
    date.fromisoformat(month + "-01")
    return [row for row in rows if row["date"].startswith(month + "-")]


def summary(rows: list[dict]) -> dict[str, int]:
    totals = defaultdict(int)
    for row in rows:
        totals[row["category"]] += row["amount_cents"]
    return dict(sorted(totals.items()))


def export_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "category", "amount", "note"])
        for row in rows:
            writer.writerow([row["date"], row["category"],
                             f'{row["amount_cents"] / 100:.2f}', row["note"]])
```

```bash
python -c 'from expense import make_expense; from reports import summary; print(summary([make_expense("2.50", "food"), make_expense("3.00", "food")]))'
git add storage.py reports.py && git diff --cached
git commit -m "feat(day1): persist JSON and calculate expense reports"
```


### Checkpoint — Inspect persistence

**Run and inspect:** After writing two records, open the JSON file and verify its exact shape. Delete the file and check that loading gives `[]`; then write malformed JSON and observe the documented error.

**Code-review discussion:** Look for an exception boundary: should a storage error be printed within `storage.py`, or reported in `main.py`? Keep presentation at the boundary.

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 3. Add a command-line interface

**Why `argparse`?** It is part of the standard library and supplies structured subcommands, required flags, validation messages, and `--help` without an extra dependency. **Why keep `main.py` thin?** A CLI should translate arguments into calls to domain, storage, and reporting functions rather than embedding the calculations itself; this keeps behavior reusable from tests and other interfaces.

**Why choose nonzero exit codes for errors?** Scripts and continuous integration can reliably distinguish success from failure. Input errors should be actionable, not raw tracebacks. Try invalid inputs deliberately before committing.


**Read this file like a reviewer — `day01_expenses/main.py`:** Find the entry point and trace the order of calls as a user executes a command. Keep it in a separate editor tab as you run the example.

**`day01_expenses/main.py`**

```python
import argparse
from pathlib import Path
from expense import make_expense
from storage import load, save
from reports import by_month, summary, export_csv


def main(argv=None):
    parser = argparse.ArgumentParser(description="Expense tracker")
    parser.add_argument("--file", type=Path, default=Path("expenses.json"))
    subs = parser.add_subparsers(dest="command", required=True)
    add = subs.add_parser("add")
    add.add_argument("--amount", required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--note", default="")
    add.add_argument("--date")
    for name in ("list", "summary", "export"):
        sub = subs.add_parser(name)
        sub.add_argument("--month")
        if name == "export":
            sub.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        rows = load(args.file)
        if args.command == "add":
            rows.append(make_expense(args.amount, args.category, args.note, args.date))
            save(args.file, rows)
            print("Expense added")
        else:
            selected = by_month(rows, args.month)
            if args.command == "list":
                for row in selected:
                    print(f'{row["date"]} {row["category"]}: {row["amount_cents"] / 100:.2f}')
            elif args.command == "summary":
                for category, cents in summary(selected).items():
                    print(f"{category}: {cents / 100:.2f}")
                print(f'TOTAL: {sum(x["amount_cents"] for x in selected) / 100:.2f}')
            else:
                export_csv(selected, args.output)
                print(f"Exported {len(selected)} records")
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

```bash
python main.py add --amount 12.50 --category food --date 2026-10-21
python main.py add --amount 8 --category travel --date 2026-10-21
python main.py summary --month 2026-10
python main.py export --output report.csv
printf '\nexpenses.json\nreport.csv\n' >> ../.gitignore
git add main.py ../.gitignore && git diff --cached
git commit -m "feat(day1): expose expense tracker CLI commands"
```


### Checkpoint — Treat the CLI as a public interface

**Run and inspect:** Call `python main.py --help`, then run add/list/summary/export. Verify that a malformed amount produces an actionable error and nonzero exit status.

**Code-review discussion:** Add an optional `--month` filter before exposing a new feature. What would break if CLI argument names changed later?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 4. Add regression tests

**Why regression tests now?** Manual checks show that a happy-path example works once. Automated tests preserve expected behavior as the code changes and make later refactors less risky. Include boundary cases: zero, negative and over-precise amounts, malformed JSON, invalid dates, and empty reports.

**Why temporary directories in tests?** They isolate test files from real user data and automatically clean up, so repeated test runs remain reproducible. Tests should not depend on yesterday's `expenses.json`.


**Read this file like a reviewer — `day01_expenses/tests/test_expenses.py`:** Identify the arrange/act/assert phases; add one boundary case before you commit. Keep it in a separate editor tab as you run the example.

**`day01_expenses/tests/test_expenses.py`**

```python
import tempfile
from pathlib import Path
import pytest
from expense import make_expense, to_cents
from reports import summary, by_month
from storage import load, save
from main import main


def test_amount_validation():
    assert to_cents("12.50") == 1250
    for bad in ("0", "-1", "NaN", "1.234", "oops"):
        with pytest.raises(ValueError):
            to_cents(bad)


def test_report_and_roundtrip(tmp_path):
    rows = [make_expense("10", " FOOD ", when="2026-10-21"),
            make_expense("3", "travel", when="2026-09-01")]
    path = tmp_path / "expenses.json"
    save(path, rows)
    assert load(path) == rows
    assert summary(by_month(rows, "2026-10")) == {"food": 1000}


def test_cli_add(tmp_path):
    path = tmp_path / "data.json"
    assert main(["--file", str(path), "add", "--amount", "2.50",
                 "--category", "food", "--date", "2026-10-21"]) == 0
    assert load(path)[0]["amount_cents"] == 250
```

```bash
python -m pytest -q tests/
git add tests/test_expenses.py && git diff --cached
git commit -m "test(day1): verify expense validation, reporting, and CLI"
cd ..
```

**Stretch:** add per-record IDs and `delete --id`, then commit the feature and its tests separately.

---


### Checkpoint — Check tests prove behavior

**Run and inspect:** Temporarily replace a comparison with the wrong operator. At least one test should fail. Restore the code and rerun. This is a lightweight way to evaluate whether assertions catch realistic regressions.

**Code-review discussion:** Why does a round-trip JSON test provide more confidence than simply checking that the file exists?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

# Day 2 — Library Management with OOP

## Your mission and definition of done

**End product:** Model behavior and invariants in collaborating classes.

**Core review concepts:** `@dataclass`; `__post_init__`; attributes and methods; composition; invariants; exception propagation.

**Definition of done:** You should be able to explain who owns the book availability rule, why a library has books instead of inheriting from Book, and which changes require a new test.

**Scope boundary:** Persistence is intentionally lightweight and not designed for simultaneous users.

### How to approach every step

1. Read the rationale before opening the editor. Predict the shape of the input and output.
2. Create the named file exactly where the guide says, and enter the full code block.
3. Execute the smoke-test command, then deliberately try one invalid input.
4. Run tests where available, inspect `git status` and `git diff --cached`, and commit only the milestone's files.
5. Write down one design trade-off you would discuss during a code review.

**Commit convention:** `feat` for behavior, `test` for tests, `refactor` for restructuring without changed behavior, `docs` for documentation, and `chore` for tooling and setup. Hashes on your machine will naturally differ from another repository's.


**Learn:** `@dataclass`, objects, encapsulation, composition, exceptions, persistence, testing.


## Guided lab: reason about entities before coding

A book is a *thing with state* (`isbn`, `title`, `available`), while borrowing is a *change governed by rules*. Sketch the relationship before implementing it:

```text
Library
  books: dict[isbn, Book]
  members: dict[member_id, Member]
  loans: ...
       borrow(book_id, member_id)
       return_book(book_id, member_id)
```

**Why not put every rule on `Book`?** A book object can guard its own fields, but it cannot know whether a supplied member exists unless you give it access to the library's member collection. Keep rules involving several entities in a coordinating `Library` object.

**Manual probe after you create `models.py`:**

```bash
python -c 'from models import Book; print(Book("978-A", "Python Patterns"))'
python -c 'from models import Book; Book("", "Missing ID")'
```

The first command should display a `Book(...)` representation. The second should fail with `ValueError`. An intentional failure demonstrates that an invariant is enforced, not that your setup is broken.

**Developer question:** Should availability be mutable on `Book`, or always derived from active loans? Both can work, but storing the same truth twice creates a risk of inconsistency. The exercise keeps the simpler representation and tests transitions carefully.

## Step 1. Model books and members

**Why `@dataclass`?** These classes mostly represent structured data. Dataclasses generate the constructor, representation, and comparison behavior so you can focus on meaningful validation. `__post_init__` enforces basic invariants immediately after construction. Use ordinary classes when initialization or lifecycle behavior becomes more involved.


```bash
mkdir -p day02_library/tests && cd day02_library
```

**Read this file like a reviewer — `day02_library/models.py`:** Locate the state fields and any validation in `__post_init__`. Ask what happens if you construct an invalid object. Keep it in a separate editor tab as you run the example.

**`day02_library/models.py`**

```python
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
```

```bash
python -c 'from models import Book; print(Book("978-1", "Clean Code"))'
git add models.py && git commit -m "feat(day2): model library entities with dataclasses"
```


### Checkpoint — Probe object invariants

**Run and inspect:** Construct a valid `Book`, inspect its `repr`, then try an empty ISBN. Ensure invalid state cannot be created quietly.

**Code-review discussion:** Compare a dataclass with a normal class: what boilerplate did Python generate, and what did it not generate?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 2. Implement business rules using composition

**Why composition instead of inheritance?** A library **has** books, members, and loans; it is not a specialized kind of book or member. Composition represents that relationship naturally and avoids brittle inheritance hierarchies. Dictionaries indexed by IDs make lookups straightforward and typically constant-time; the library service is the right place for cross-entity rules such as blocking duplicate loans.

**Why raise exceptions for domain rule violations?** Borrowing a missing or already checked-out book must not silently succeed. Clear exceptions let a future web or CLI layer choose how to present errors without complicating the domain model.


**Read this file like a reviewer — `day02_library/library.py`:** Locate the methods that mutate availability. Ask which method prevents a second loan for the same book. Keep it in a separate editor tab as you run the example.

**`day02_library/library.py`**

```python
from dataclasses import asdict
from models import Book, Member


class Library:
    def __init__(self):
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        self.loans: dict[str, str] = {}  # isbn -> member_id

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
            raise ValueError("Book is already borrowed")
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
        return {"books": [asdict(book) for book in self.books.values()],
                "members": [asdict(member) for member in self.members.values()],
                "loans": self.loans.copy()}
```

**Read this file like a reviewer — `day02_library/main.py`:** Find the entry point and trace the order of calls as a user executes a command. Keep it in a separate editor tab as you run the example.

**`day02_library/main.py`**

```python
from library import Library
from models import Book, Member


def main():
    library = Library()
    library.add_book(Book("978-1", "Clean Code"))
    library.register(Member("m1", "Alice"))
    library.borrow("978-1", "m1")
    print("After borrowing:", library.snapshot())
    library.return_book("978-1")
    print("Available:", [book.title for book in library.available_books()])


if __name__ == "__main__":
    main()
```

```bash
python main.py
git add library.py main.py && git commit -m "feat(day2): implement borrowing rules using composition"
```


### Checkpoint — Trace loan transitions

**Run and inspect:** Add a book and member; borrow once; try borrowing the same book again; return it; borrow again. Identify exactly which object owns every state change.

**Code-review discussion:** If you add a reservation queue, would the Book class need to know about Members? Justify your service boundary.

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 3. Persist library state and test domain rules

**Why serialize explicit state?** Persist the information needed to reconstruct a working library rather than attempting to serialize arbitrary object internals. A save/load round-trip test checks that the reconstructed objects preserve borrowing behavior, not merely that a file exists.


**Read this file like a reviewer — `day02_library/persistence.py`:** Track the data path from Python objects to serialized data and back. Identify which fields must survive a round trip. Keep it in a separate editor tab as you run the example.

**`day02_library/persistence.py`**

```python
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
    if any(isbn not in library.books or member not in library.members
           for isbn, member in library.loans.items()):
        raise ValueError("Invalid loan references")
    if any(book.available == (isbn in library.loans)
           for isbn, book in library.books.items()):
        raise ValueError("Inconsistent book availability")
    return library
```

**Read this file like a reviewer — `day02_library/tests/test_library.py`:** Look for tests of invalid operations, not just successful borrowing and returning. Keep it in a separate editor tab as you run the example.

**`day02_library/tests/test_library.py`**

```python
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
```

```bash
python -m pytest -q tests/
git add persistence.py tests/test_library.py
git commit -m "test(day2): persist state and enforce borrowing invariants"
cd ..
```

**Stretch:** add loan dates and overdue rules without changing `Book` or `Member` excessively.

---


### Checkpoint — Round-trip check

**Run and inspect:** Persist non-empty library state, load it, and verify that current book availability remains correct. Tests of persistence should assert the reconstructed *behavior*, not just the file contents.

**Code-review discussion:** How would saving midway through a write affect the file? What stronger storage strategy might a multi-user system need?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 4 — Professional review, debugging, and extra challenges

### 4.1 Inspect the actual saved state

Use a temporary directory when experimenting with persistence. In a Python REPL, create a library, add a book and member, borrow the book, save it, reload it, and inspect the reloaded book's availability. The persistence functions in this chapter show the exact signatures; adapt the example to those names rather than guessing.

**Expected invariant:** a borrowed book must still be unavailable after reloading, and a returned book must become available again. If the program instead creates two sources of truth for availability, your tests need to detect that divergence.

### 4.2 Reason about a failed borrow

Before calling the borrow method, list the conditions that must be true: the book exists, the member exists, and the book is currently available. Then try violating one condition at a time.

```python
# Independent reasoning exercise: a deliberately tiny rule.
def can_borrow(book_exists: bool, member_exists: bool, available: bool) -> bool:
    return book_exists and member_exists and available

assert can_borrow(True, True, True)
assert not can_borrow(True, False, True)
assert not can_borrow(True, True, False)
```

This helper is **not** a replacement for the class implementation. It is an exercise in translating business conditions into explicit tests.

### 4.3 Why exceptions beat special return values for broken invariants

If `borrow()` returns `None` for a missing book but also returns `None` when it succeeds, callers cannot tell what happened without inspecting unrelated state. A clearly documented exception communicates failure and keeps the success path simpler. Conversely, an expected search that returns no results may legitimately return `[]`: not every absence deserves an exception.

### 4.4 Try a regression test before fixing a bug

Choose a rule such as "the same book cannot be borrowed twice." First add a test that performs two borrow attempts and asserts the second fails. Verify it fails if you intentionally remove the rule, then restore the rule.

```bash
# Run from the day02_library directory
python -m pytest -v tests/
git status
git diff --check
```

### 4.5 Review the design with a teammate

Ask: Where are identifiers validated? Can a member borrow a nonexistent book? What happens if persistence fails? Would it be safe to expose mutable dictionaries publicly? Does a `Book` know too much about `Library`? Write answers in `day02_library/NOTES.md` and commit them if they help future readers.

```bash
git add NOTES.md
git diff --cached
git commit -m "docs(day2): record object model invariants and tradeoffs"
```

### Day 2 independent challenges

- [ ] Prevent an unavailable book from being borrowed twice.
- [ ] Add a count of available books.
- [ ] List all active loans.
- [ ] Validate that member IDs cannot consist entirely of whitespace.
- [ ] Add tests for persistence after a return.
- [ ] Explain when a database would be better than file-based persistence.

**Ready for Day 3 when:** You can draw the object model, explain each ownership boundary, and run the entire test suite without relying on previously generated files.

---


# Day 3 — Streaming Log Analyzer

## Your mission and definition of done

**End product:** Analyze data too large to load at once.

**Core review concepts:** iterables versus iterators; `yield`; exception-tolerant parsing; Counter; decorators; timing.

**Definition of done:** You should be able to explain when the generator executes, why `list(generator)` discards the streaming advantage, and why a timer decorator preserves metadata.

**Scope boundary:** The sample log format is simplified; realistic web-server logs need a more robust parser.

### How to approach every step

1. Read the rationale before opening the editor. Predict the shape of the input and output.
2. Create the named file exactly where the guide says, and enter the full code block.
3. Execute the smoke-test command, then deliberately try one invalid input.
4. Run tests where available, inspect `git status` and `git diff --cached`, and commit only the milestone's files.
5. Write down one design trade-off you would discuss during a code review.

**Commit convention:** `feat` for behavior, `test` for tests, `refactor` for restructuring without changed behavior, `docs` for documentation, and `chore` for tooling and setup. Hashes on your machine will naturally differ from another repository's.


**Learn:** generators, `yield`, decorators, `Counter`, `contextmanager`, regex, memory-efficient streaming.


## Guided lab: see lazy evaluation rather than memorizing it

Before editing the log parser, prove to yourself that generators do not execute immediately:

```python
def numbers():
    print("generator started")
    yield 10
    print("after first yield")
    yield 20

items = numbers()          # nothing printed yet
print(next(items))         # generator started, then 10
print(next(items))         # after first yield, then 20
```

**Why this matters:** The parser can hand the analyzer one log record at a time instead of allocating an enormous list. But the aggregator still retains whatever statistics you decide to keep; streaming avoids keeping every *input record*, not all possible memory growth.

**Investigate:** What happens if you call `list(parse_logs(...))` before passing the result into the analyzer? Your program will work on small files, but memory becomes proportional to the number of records.

**Quality gate:** In a real monitoring system you would record malformed-line counts and provide an error threshold. Silently skipping every bad line can produce falsely reassuring statistics.

## Step 1. Parse logs lazily

**Why `yield` instead of returning a list?** A generator produces records one at a time. Streaming uses memory proportional to a small amount of parser state rather than the whole input file, which matters for large logs. The generator runs only when iterated. Here malformed lines are skipped for simplicity; production logging pipelines should count, surface, or quarantine them so missing data is observable.


```bash
mkdir -p day03_logs/tests && cd day03_logs
```

Use this simplified log format: `IP STATUS DURATION_MS`.

**`day03_logs/sample.log`**

```text
10.0.0.1 200 15
10.0.0.2 500 130
10.0.0.1 404 45
10.0.0.1 200 25
```

**Read this file like a reviewer — `day03_logs/parser.py`:** Find the `yield` statement. Compare calling the generator with actually iterating it. Keep it in a separate editor tab as you run the example.

**`day03_logs/parser.py`**

```python
from pathlib import Path
from typing import Iterator


def read_logs(path: Path) -> Iterator[dict]:
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            parts = line.split()
            if len(parts) != 3:
                continue  # In production, record malformed lines in logs.
            ip, status, duration = parts
            try:
                yield {"ip": ip, "status": int(status),
                       "duration_ms": int(duration), "line": line_number}
            except ValueError:
                continue
```

```bash
python -c 'from pathlib import Path; from parser import read_logs; print(list(read_logs(Path("sample.log"))))'
git add sample.log parser.py && git commit -m "feat(day3): stream and parse log records lazily"
```


### Checkpoint — Inspect input handling

**Run and inspect:** Run the parser on valid and malformed lines. Count how many events were emitted, and identify which fields were extracted.

**Code-review discussion:** What if logs are compressed or split across files? Which layer should handle decompression?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 2. Analyze streams and measure execution time

**Why `Counter`?** It is designed for counting occurrences, making IP and status tallies shorter and clearer than handwritten dictionary initialization. **Why `functools.wraps` in a decorator?** It preserves the wrapped function's name and metadata, which improves introspection, debugging, and tooling. **Why `perf_counter`?** It measures elapsed duration using a high-resolution monotonic clock; a single measurement is illustrative, not a rigorous benchmark.


**Read this file like a reviewer — `day03_logs/analyzer.py`:** Follow a record from parser output into the counters, then examine what the timing decorator returns. Keep it in a separate editor tab as you run the example.

**`day03_logs/analyzer.py`**

```python
from collections import Counter
from functools import wraps
from time import perf_counter


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__}: {perf_counter() - start:.4f}s")
    return wrapper


@timed
def analyze(records, slow_threshold: int = 100) -> dict:
    ip_counts = Counter()
    status_counts = Counter()
    slow = 0
    total = 0
    for row in records:
        total += 1
        ip_counts[row["ip"]] += 1
        status_counts[row["status"]] += 1
        slow += row["duration_ms"] >= slow_threshold
    return {"total": total, "top_ips": ip_counts.most_common(5),
            "status_counts": dict(status_counts), "slow_requests": slow}
```

**Read this file like a reviewer — `day03_logs/main.py`:** Find the entry point and trace the order of calls as a user executes a command. Keep it in a separate editor tab as you run the example.

**`day03_logs/main.py`**

```python
import argparse
import json
from pathlib import Path
from parser import read_logs
from analyzer import analyze


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--slow-ms", type=int, default=100)
    args = parser.parse_args()
    print(json.dumps(analyze(read_logs(args.path), args.slow_ms), indent=2))


if __name__ == "__main__":
    main()
```

```bash
python main.py sample.log --slow-ms 100
git add analyzer.py main.py && git commit -m "feat(day3): aggregate request metrics and time execution"
```


### Checkpoint — Verify aggregate math

**Run and inspect:** Calculate the expected count for each status in the sample by hand. Compare with the summary.

**Code-review discussion:** A decorator measures runtime, but does not change the returned analysis result: why is that valuable?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 3. Verify large-file behavior

**Why test generators and edge cases?** It is easy to accidentally call `list()` and eliminate streaming's memory advantage. Tests should prove valid input is counted correctly, malformed input is handled predictably, and a generator is consumed as intended. To compare memory usage, measure under representative file sizes rather than inferring it from wall-clock time alone.


**Read this file like a reviewer — `day03_logs/tests/test_logs.py`:** Identify tests for malformed records and confirm output on the representative sample. Keep it in a separate editor tab as you run the example.

**`day03_logs/tests/test_logs.py`**

```python
from parser import read_logs
from analyzer import analyze


def test_log_analysis(tmp_path):
    path = tmp_path / "requests.log"
    path.write_text("a 200 10\na 500 150\nb 404 25\nmalformed\n", encoding="utf-8")
    result = analyze(read_logs(path), slow_threshold=100)
    assert result["total"] == 3
    assert result["top_ips"][0] == ("a", 2)
    assert result["status_counts"][500] == 1
    assert result["slow_requests"] == 1


def test_empty_file(tmp_path):
    path = tmp_path / "empty.log"
    path.write_text("", encoding="utf-8")
    assert analyze(read_logs(path))["total"] == 0
```

```bash
python -m pytest -q tests/
git add tests/test_logs.py && git commit -m "test(day3): cover streaming, malformed lines, and summaries"
cd ..
```

**Stretch:** generate a million-line sample file and measure peak memory usage with `tracemalloc`.

---


### Checkpoint — Think about scale

**Run and inspect:** Generate a larger synthetic log locally and compare stream parsing to `list(...)` using a profiler if available.

**Code-review discussion:** Why might a single bad regex or unbounded `Counter` still cause problems despite the generator?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 4 — Observe memory behavior and log-quality trade-offs

### 4.1 A tiny streaming experiment

Create `stream_demo.py` alongside the parser; this is a disposable learning exercise, not part of the main application.

```python
from pathlib import Path


def lines(path: Path):
    with path.open(encoding="utf-8") as file:
        for line in file:
            yield line.rstrip("\n")


for line in lines(Path("sample.log")):
    print(line)
```

Run it with `python stream_demo.py`, then change the loop to `all_lines = list(lines(Path("sample.log")))`. Both print the same small example; only the latter materializes every line at once.

**Why is this not a proof of performance?** A three-line file is too small to measure meaningfully. Use a representative file and a profiler when evaluating memory or speed.

### 4.2 Make parser failure visible

Consider two policies: skip malformed lines and count them, or fail immediately. Skipping supports operational continuity, but can hide widespread data corruption. Failing gives stricter guarantees but can stop reporting entirely. The right policy depends on whether a log summary is advisory or feeds critical billing/security decisions.

```python
# Small independent pattern for a quality counter.
from collections import Counter

quality = Counter()
for raw in ["200", "404", "bad", "500"]:
    try:
        status = int(raw)
    except ValueError:
        quality["malformed"] += 1
    else:
        quality["parsed"] += 1

print(quality)  # Counter({'parsed': 3, 'malformed': 1})
```

### 4.3 Validate a decorator's transparency

A correctly designed timing decorator should preserve the wrapped function's return value and propagate its exceptions. Test that explicitly rather than only inspecting printed timing output. Use `functools.wraps` so documentation tools and debugging still see the original function's metadata.

### 4.4 Know what the counters cost

Streaming logs can keep input memory low, but a `Counter` with a unique key for each of millions of IP addresses may still grow large. The memory bound is approximately the number of distinct keys retained, not the total number of lines read. For very high cardinality, discuss database aggregation, bounded top-K structures, or approximate sketches.

### 4.5 Clean up and commit

Delete the disposable `stream_demo.py`, or retain it under a clearly named `examples/` directory with an explanatory README. Do not accidentally commit a massive generated log file.

```bash
python -m pytest -q tests/
git status
git diff --check
# Only stage tracked source or intentional learning examples.
```

### Day 3 independent challenges

- [ ] Count malformed log lines instead of silently discarding them.
- [ ] Add an option to filter 4xx and 5xx responses.
- [ ] Print the three busiest IP addresses.
- [ ] Support a custom input filename.
- [ ] Add a test with an empty log file.
- [ ] Explain why `yield from` can simplify combining several generators.

**Ready for Day 4 when:** You can explain generator laziness, prove sample totals, and articulate the limitations of your parser.

---


# Day 4 — Algorithms and Async API Aggregator

## Your mission and definition of done

**End product:** Solve small algorithms and overlap HTTP wait time.

**Core review concepts:** hash maps; binary search; Big-O; `async def`; `await`; `asyncio.gather`; semaphores; HTTP failure handling.

**Definition of done:** You should be able to justify O(n) versus O(n²), state the preconditions of binary search, and explain why request concurrency needs a limit.

**Scope boundary:** Async improves I/O scheduling, not CPU-intensive Python execution by itself.

### How to approach every step

1. Read the rationale before opening the editor. Predict the shape of the input and output.
2. Create the named file exactly where the guide says, and enter the full code block.
3. Execute the smoke-test command, then deliberately try one invalid input.
4. Run tests where available, inspect `git status` and `git diff --cached`, and commit only the milestone's files.
5. Write down one design trade-off you would discuss during a code review.

**Commit convention:** `feat` for behavior, `test` for tests, `refactor` for restructuring without changed behavior, `docs` for documentation, and `chore` for tooling and setup. Hashes on your machine will naturally differ from another repository's.


**Learn:** hash maps, Big-O, async/await, `asyncio.gather`, HTTP clients, timeouts, concurrency limits, mocking.


## Guided lab: measure what async actually changes

First, reason about an I/O timeline:

```text
Sequential: request A [wait] -> request B [wait] -> request C [wait]
Concurrent: request A [wait]--------------------
            request B [wait]--------------------
            request C [wait]--------------------
```

**Why this matters:** `asyncio` overlaps waiting, but a single event loop still needs tasks to yield control at `await` points. A CPU-heavy loop without `await` can block all other coroutines.

Try this standard-library experiment independently:

```python
import asyncio
import time

async def fake_request(name: str) -> str:
    await asyncio.sleep(0.1)
    return name

async def run():
    start = time.perf_counter()
    result = await asyncio.gather(
        fake_request("A"), fake_request("B"), fake_request("C")
    )
    print(result)
    print("elapsed:", round(time.perf_counter() - start, 2))

asyncio.run(run())
```

Expected result includes `['A', 'B', 'C']`; the measured duration varies by machine and is not a guaranteed benchmark number. Compare it to awaiting the same calls one after another.

**Review question:** If a server allows only three concurrent calls, what might happen when 500 clients start a request together? This is why semaphores, backoff, and server-provided rate limits matter.

## Step 1. Write and test algorithms

**Why use a hash map for Two Sum?** Recording previously seen numbers trades additional memory for a single linear pass: expected O(n) time instead of checking every pair in O(n²). **Why binary search?** Halving the remaining range gives O(log n) time, but only when the input is already sorted. State preconditions explicitly; fast code on unsorted data is simply wrong.


```bash
mkdir -p day04_async/tests && cd day04_async
```

**Read this file like a reviewer — `day04_async/algorithms.py`:** For each algorithm, write its input preconditions and time complexity before running it. Keep it in a separate editor tab as you run the example.

**`day04_async/algorithms.py`**

```python

def two_sum(numbers: list[int], target: int) -> tuple[int, int] | None:
    seen = {}
    for index, value in enumerate(numbers):
        match = target - value
        if match in seen:
            return seen[match], index
        seen[value] = index
    return None  # O(n) time, O(n) auxiliary space


def binary_search(sorted_numbers: list[int], target: int) -> int:
    left, right = 0, len(sorted_numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if sorted_numbers[mid] == target:
            return mid
        if sorted_numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # O(log n) time
```

```bash
python -c 'from algorithms import two_sum, binary_search; assert two_sum([2,7,11],9)==(0,1); assert binary_search([1,3,5],3)==1'
git add algorithms.py && git commit -m "feat(day4): implement hash-map and binary-search algorithms"
```


### Checkpoint — Check complexity claims

**Run and inspect:** Write down O(n) expected time and O(n) space for a hash-map Two Sum solution, and O(log n) time for binary search on sorted data.

**Code-review discussion:** What is the behavior if the array is unsorted? Should the algorithm sort it or document the precondition?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 2. Fetch API data concurrently

**Why `asyncio` here?** HTTP requests spend much of their time waiting for network responses; asynchronous concurrency overlaps that waiting. It does not make CPU-heavy Python calculations automatically faster. `asyncio.gather` preserves the order of submitted requests in its returned results, and the semaphore caps simultaneous requests to avoid overwhelming an API.

**Why use one shared `httpx.AsyncClient`?** It can reuse connections and centralizes timeouts. `raise_for_status()` turns HTTP error responses into exceptions you can handle. Production clients may additionally need retries with backoff, rate-limit handling, authentication, and cancellation behavior.


**Read this file like a reviewer — `day04_async/aggregator.py`:** Circle each `await`, the shared client, and the concurrency limit. Trace errors for a failed response. Keep it in a separate editor tab as you run the example.

**`day04_async/aggregator.py`**

```python
import asyncio
import json
import httpx

URLS = [
    "https://jsonplaceholder.typicode.com/todos/1",
    "https://jsonplaceholder.typicode.com/todos/2",
    "https://jsonplaceholder.typicode.com/todos/3",
]


async def fetch_one(client: httpx.AsyncClient, url: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return {"url": url, "data": response.json(), "error": None}
        except (httpx.HTTPError, ValueError) as exc:
            return {"url": url, "data": None, "error": str(exc)}


async def aggregate(urls: list[str], max_concurrent: int = 3) -> list[dict]:
    if max_concurrent < 1:
        raise ValueError("max_concurrent must be positive")
    semaphore = asyncio.Semaphore(max_concurrent)
    async with httpx.AsyncClient(timeout=10.0) as client:
        return await asyncio.gather(
            *(fetch_one(client, url, semaphore) for url in urls)
        )


if __name__ == "__main__":
    print(json.dumps(asyncio.run(aggregate(URLS)), indent=2))
```

```bash
python aggregator.py  # Requires Internet access for the public demo API.
git add aggregator.py && git commit -m "feat(day4): fetch HTTP resources concurrently with limits"
```


### Checkpoint — Observe failures

**Run and inspect:** Try a healthy endpoint, an HTTP error response, and an unreachable host; compare the exception types.

**Code-review discussion:** What is the maximum number of requests in flight? Do you share one client or create one per task?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 3. Test async code without using the network

**Why mock HTTP responses?** Public APIs can fail, change, or rate-limit you, making test results unreliable. A mocked transport makes successful and failing responses deterministic and lets you check behavior while offline. Keep a separate optional integration test for the real service.


**Read this file like a reviewer — `day04_async/tests/test_async.py`:** Find how network calls are faked. Keep normal tests network-independent. Keep it in a separate editor tab as you run the example.

**`day04_async/tests/test_async.py`**

```python
import asyncio
import httpx
import pytest
from algorithms import two_sum, binary_search
from aggregator import fetch_one, aggregate


def test_algorithms():
    assert two_sum([3, 2, 4], 6) == (1, 2)
    assert binary_search([1, 2, 3], 9) == -1


def test_mocked_async_fetch():
    def handler(request):
        return httpx.Response(200, json={"ok": True})

    async def run():
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as client:
            result = await fetch_one(client, "https://example.test/data", asyncio.Semaphore(1))
        assert result["data"] == {"ok": True}
        assert result["error"] is None

    asyncio.run(run())


def test_invalid_concurrency():
    with pytest.raises(ValueError):
        asyncio.run(aggregate(["https://example.test"], 0))
```

```bash
python -m pytest -q tests/
git add tests/test_async.py && git commit -m "test(day4): mock HTTP requests and validate algorithms"
cd ..
```

**Stretch:** benchmark sequential vs concurrent requests, then add exponential backoff for transient HTTP errors.

---


### Checkpoint — Verify deterministic tests

**Run and inspect:** Run the tests twice with networking disabled. If the tests depend on a public website, refactor them to use a mocked transport.

**Code-review discussion:** What evidence would you need before claiming asynchronous execution is faster for this workload?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 4 — Benchmark and failure-handling workshop

### 4.1 Write the sequential baseline first

Use a controlled simulated I/O workload to see the difference between sequential and concurrent scheduling.

```python
import asyncio
import time


async def request(n: int) -> int:
    await asyncio.sleep(0.05)
    return n * 2


async def sequential():
    return [await request(i) for i in range(5)]


async def concurrent():
    return await asyncio.gather(*(request(i) for i in range(5)))


async def main():
    for name, fn in [("sequential", sequential), ("concurrent", concurrent)]:
        start = time.perf_counter()
        result = await fn()
        print(name, result, round(time.perf_counter() - start, 3))


asyncio.run(main())
```

Both functions return `[0, 2, 4, 6, 8]`. The concurrent version will generally finish the simulated waits sooner, but don't rely on precise timings across machines.

### 4.2 Why sharing a client matters

An HTTP client can pool connections and centralize timeout settings. Opening and closing a new client for every request discards these benefits and can put extra pressure on socket resources. A shared client must still be closed through its asynchronous context manager.

### 4.3 Design the error contract

Choose one policy for an API failure: abort the entire operation, return partial results plus errors, or retry eligible failures. None is universally right. A financial report might require complete data; a dashboard might prefer partial results with an explicit warning. A retry should use a bounded attempt count and backoff so temporary failures don't produce unbounded load.

### 4.4 Unit test errors without the Internet

Use a mocked HTTP transport to return status 503, a malformed payload, and a normal success. Assert either the documented exception or the returned error structure. An offline test should pass even if the public API changes or the machine has no connection.

```bash
python -m pytest -v tests/
git status
git diff --cached
```

### 4.5 Understand `gather` ordering

If tasks have different completion times, `asyncio.gather` still returns its list in the order of the input awaitables. If you need to process each result immediately as it finishes, investigate `asyncio.as_completed`; account for error and cancellation handling before adopting it.

### Day 4 independent challenges

- [ ] Compare linear versus binary search on sorted input.
- [ ] Write a Two Sum test with duplicated numbers.
- [ ] Add a `max_concurrency` setting to the aggregator.
- [ ] Make an HTTP 500 test deterministic.
- [ ] Test the empty endpoint list.
- [ ] Explain why async alone does not accelerate CPU-bound image processing.

**Ready for Day 5 when:** You can explain the expected complexity of the algorithms and distinguish I/O concurrency from CPU parallelism.

---


# Day 5 — Task Manager REST API

## Your mission and definition of done

**End product:** Make a database-backed API that others can call.

**Core review concepts:** SQL tables; parameter placeholders; constraints; HTTP methods; Pydantic schemas; `TestClient`; SQLite.

**Definition of done:** You should be able to create/read/update/delete a task, describe a 404 versus a 422 response, and explain why raw string interpolation in SQL is unsafe.

**Scope boundary:** SQLite is ideal for the exercise; production deployments need connection management, migrations, and authorization.

### How to approach every step

1. Read the rationale before opening the editor. Predict the shape of the input and output.
2. Create the named file exactly where the guide says, and enter the full code block.
3. Execute the smoke-test command, then deliberately try one invalid input.
4. Run tests where available, inspect `git status` and `git diff --cached`, and commit only the milestone's files.
5. Write down one design trade-off you would discuss during a code review.

**Commit convention:** `feat` for behavior, `test` for tests, `refactor` for restructuring without changed behavior, `docs` for documentation, and `chore` for tooling and setup. Hashes on your machine will naturally differ from another repository's.


**Learn:** REST, FastAPI, Pydantic, SQLite, CRUD, HTTP status codes, schema validation.


## Guided lab: trace a request all the way to storage

Think in layers rather than starting with decorators:

```text
POST /tasks
  -> FastAPI parses JSON
  -> Pydantic validates fields
  -> endpoint calls SQL code
  -> SQLite stores a row
  -> endpoint returns JSON + HTTP status
```

**Why separate HTTP validation from database constraints?** Pydantic provides readable feedback to API callers. Database constraints provide a second safety boundary if another code path writes data later. The two layers have different responsibilities.

After you start the server, open `http://127.0.0.1:8000/docs` to inspect the automatically generated OpenAPI interface, or exercise the API from another terminal:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Review type hints"}'

curl http://127.0.0.1:8000/tasks
```

**Read the actual schema in the code before trying the request.** If your task schema requires more fields, supply them explicitly. The specific generated task ID depends on database state.

**Debugging checklist:** A 422 response points to request validation; a 404 indicates a missing resource; a 500 indicates a server-side failure. Inspect the response body and server log rather than guessing.

## Step 1. Create the data layer

**Why introduce SQLite after JSON?** A relational database supports structured queries, filtering, constraints, and safer concurrent access patterns as the dataset grows. SQLite is built into Python and requires no database server, so it is ideal for learning SQL. **Why placeholders (`?`) in queries?** Parameterized SQL separates untrusted values from SQL syntax, preventing SQL injection through those parameters.


```bash
mkdir -p day05_tasks/tests && cd day05_tasks
```

**Read this file like a reviewer — `day05_tasks/db.py`:** Identify where the database connection is created and closed and where schema initialization happens. Keep it in a separate editor tab as you run the example.

**`day05_tasks/db.py`**

```python
import sqlite3
from pathlib import Path


def connect(db_path: str | Path):
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    """)
    connection.commit()
    return connection
```

```bash
python -c 'from db import connect; c=connect(":memory:"); print(c.execute("SELECT name FROM sqlite_master WHERE type=\x27table\x27").fetchall())'
git add db.py && git commit -m "feat(day5): create SQLite task storage schema"
```


### Checkpoint — Inspect actual SQL

**Run and inspect:** Look at the schema and identify primary keys and defaults. Try inserting invalid data intentionally and see which layer catches it.

**Code-review discussion:** How does a parameter placeholder differ from interpolating the input into a query string?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 2. Build FastAPI CRUD endpoints

**Why use Pydantic request models?** They validate and document API inputs automatically, giving clients useful errors before business logic executes. Separate request and response models prevent clients from arbitrarily supplying server-managed fields such as a database ID. **Why distinguish HTTP methods?** POST creates, GET reads, PUT updates, and DELETE removes resources, making the API predictable for callers.

**Why paginate?** Returning an unbounded number of rows becomes increasingly slow and memory-intensive. `limit` and `offset` keep responses manageable; large datasets often benefit from keyset pagination later.


**Read this file like a reviewer — `day05_tasks/app.py`:** Follow one handler from request validation through persistence to the response. Note which failures become HTTP errors. Keep it in a separate editor tab as you run the example.

**`day05_tasks/app.py`**

```python
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from db import connect

app = FastAPI(title="Task Manager")


class TaskInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class Task(TaskInput):
    id: int


def get_db():
    return connect(os.environ.get("TASK_DB", "tasks.db"))


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskInput):
    with get_db() as db:
        cursor = db.execute("INSERT INTO tasks(title, done) VALUES (?, ?)",
                            (payload.title, int(payload.done)))
        return Task(id=cursor.lastrowid, **payload.model_dump())


@app.get("/tasks", response_model=list[Task])
def list_tasks(done: bool | None = None, limit: int = 50, offset: int = 0):
    if not 1 <= limit <= 100 or offset < 0:
        raise HTTPException(422, "Invalid pagination")
    sql = "SELECT id, title, done FROM tasks"
    params: list = []
    if done is not None:
        sql += " WHERE done = ?"
        params.append(int(done))
    sql += " ORDER BY id LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    with get_db() as db:
        return [Task(id=row["id"], title=row["title"], done=bool(row["done"]))
                for row in db.execute(sql, params)]


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskInput):
    with get_db() as db:
        result = db.execute("UPDATE tasks SET title=?, done=? WHERE id=?",
                            (payload.title, int(payload.done), task_id))
        if result.rowcount == 0:
            raise HTTPException(404, "Task not found")
        return Task(id=task_id, **payload.model_dump())


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_db() as db:
        result = db.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        if result.rowcount == 0:
            raise HTTPException(404, "Task not found")
```

```bash
fastapi dev app.py
# Open http://127.0.0.1:8000/docs in a browser, then stop the server (Ctrl+C).
git add app.py && git commit -m "feat(day5): implement Task Manager REST CRUD endpoints"
```


### Checkpoint — Exercise HTTP status codes

**Run and inspect:** Try one valid create, one invalid create, one missing ID, and one listing request. Inspect response bodies, not just status codes.

**Code-review discussion:** Do create and update requests have exactly the same shape? When might separate Pydantic schemas be clearer?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 3. Test the API with a temporary database

**Why isolate database state during tests?** Tests that share the normal development database can be order-dependent or destroy real records. A temporary database gives each test run a predictable starting state. Cover not-found responses and validation errors as well as successful CRUD flows.


**Read this file like a reviewer — `day05_tasks/tests/test_api.py`:** Note how the test database is isolated and how HTTP requests assert status codes. Keep it in a separate editor tab as you run the example.

**`day05_tasks/tests/test_api.py`**

```python
import os
from fastapi.testclient import TestClient
from app import app


def test_task_lifecycle(tmp_path, monkeypatch):
    monkeypatch.setenv("TASK_DB", str(tmp_path / "test.db"))
    client = TestClient(app)
    created = client.post("/tasks", json={"title": "Learn FastAPI"})
    assert created.status_code == 201
    task_id = created.json()["id"]
    assert len(client.get("/tasks").json()) == 1
    updated = client.put(f"/tasks/{task_id}", json={"title": "Write tests", "done": True})
    assert updated.status_code == 200
    assert updated.json()["done"] is True
    assert client.get("/tasks", params={"done": True}).json()[0]["id"] == task_id
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.delete(f"/tasks/{task_id}").status_code == 404


def test_reject_empty_title(tmp_path, monkeypatch):
    monkeypatch.setenv("TASK_DB", str(tmp_path / "test.db"))
    assert TestClient(app).post("/tasks", json={"title": ""}).status_code == 422
```

```bash
python -m pytest -q tests/
git add tests/test_api.py && git commit -m "test(day5): verify CRUD endpoints and validation"
cd ..
```

**Stretch:** add a `GET /tasks/{id}` endpoint and status/priorities, with database migrations rather than manual table edits.

---


### Checkpoint — Check isolation

**Run and inspect:** Run tests twice; results must not depend on a database file from the preceding run.

**Code-review discussion:** Would a production DB migration be safe if existing data uses the old schema?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 4 — Use the API as a client would

### 4.1 Start the server and inspect OpenAPI

From `day05_tasks`, start the FastAPI app exactly as shown earlier. Open `/docs` in a browser and compare the generated schema with your Pydantic fields. A reviewer should be able to discover how to call the API without reading the Python implementation.

### 4.2 Test a happy path

Open a second terminal. The example below assumes a `title` field is required; consult the supplied request model for additional required fields.

```bash
curl -i http://127.0.0.1:8000/tasks
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Build tests"}'
```

Record the actual HTTP status, response body, and generated identifier. Do not hardcode an ID from someone else's run; IDs are determined by the database's current contents.

### 4.3 Test failure behavior

Call an endpoint for a nonexistent task and submit a malformed payload. Expect informative client errors, not a raw Python traceback. A validation error and a missing-record error have different meanings and should not share one generic response if the API can identify them.

### 4.4 Why use parameterized SQL?

Never build a SQL statement like `f"SELECT * FROM tasks WHERE title = '{title}'"` from user input. Parameters send the value separately from the SQL syntax and prevent it from being treated as executable SQL. Parameters do **not** work for arbitrary column identifiers; accept a fixed, explicit allowlist for sort fields.

### 4.5 Why test with a temporary database?

A development database contains changeable state. If each test reads it, the tests can fail merely because a record already exists. A temporary database allows clean setup, repeatable assertions, and safe deletion at the end of testing.

```bash
python -m pytest -q tests/
git status
git diff --check
```

### Day 5 independent challenges

- [ ] Add an allowed-list filter on status.
- [ ] Reject blank task titles.
- [ ] Enforce maximum page size.
- [ ] Add a test asserting 404 for missing IDs.
- [ ] Explain what happens if two clients update the same record.
- [ ] Document three example `curl` commands in README.

**Ready for Day 6 when:** You can exercise CRUD through HTTP and follow each request into the database.

---


# Day 6 — Make the Task API Production-Minded

## Your mission and definition of done

**End product:** Make code safer to change and easier to maintain.

**Core review concepts:** services; dependency injection; mocks; logging; pytest; Ruff; GitHub Actions.

**Definition of done:** You should be able to isolate logic for unit testing, tell a unit test from an integration test, and interpret a failing CI check.

**Scope boundary:** CI and formatting are guardrails, not security audits or guarantees of correctness.

### How to approach every step

1. Read the rationale before opening the editor. Predict the shape of the input and output.
2. Create the named file exactly where the guide says, and enter the full code block.
3. Execute the smoke-test command, then deliberately try one invalid input.
4. Run tests where available, inspect `git status` and `git diff --cached`, and commit only the milestone's files.
5. Write down one design trade-off you would discuss during a code review.

**Commit convention:** `feat` for behavior, `test` for tests, `refactor` for restructuring without changed behavior, `docs` for documentation, and `chore` for tooling and setup. Hashes on your machine will naturally differ from another repository's.


**Learn:** fixtures, mocking, logging, static checks, CI, dependency isolation. This day **builds on Day 5**.


## Guided lab: understand the difference between a test double and the real system

When a service sends a notification, testing should not require a real email service. You can inject a callable:

```python
def complete_task(task_id: int, notify) -> None:
    # Example of a small seam for a test double.
    notify(f"Task {task_id} completed")
```

In a unit test, supply a `Mock` and assert the expected call. In an integration test, use real modules with a temporary database. **Why both?** A fake verifies the decision to notify, while an integration test catches broken wiring or SQL behavior that a mock can hide.

**Git workflow note:** Only commit formatting changes after inspecting their diff. Avoid hiding a functional refactor and a repository-wide reformat in one enormous commit.

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q tests/
git status
git diff --check
```

Run these commands from the relevant project directory. If a check fails, investigate rather than continuing to the next commit.

## Step 1. Extract a testable service function

**Why move logic out of endpoints?** Business functions become easier to test without constructing HTTP requests or databases. HTTP handlers can focus on translating request/response data; services enforce application rules. **Why structured logging instead of `print`?** Logging supports severity levels, centralized collection, and operational filtering, while keeping diagnostic output separate from user-visible output.


```bash
mkdir -p day06_quality/tests .github/workflows
cd day06_quality
```

**Read this file like a reviewer — `day06_quality/service.py`:** Identify where pure business logic ends and side effects such as notification or logging begin. Keep it in a separate editor tab as you run the example.

**`day06_quality/service.py`**

```python
import logging

logger = logging.getLogger(__name__)


def normalize_title(title: str) -> str:
    normalized = " ".join(title.split())
    if not normalized:
        raise ValueError("Title is required")
    if len(normalized) > 200:
        raise ValueError("Title too long")
    logger.info("Task title normalized")
    return normalized


def create_with_notifier(title: str, save, notify) -> int:
    clean = normalize_title(title)
    task_id = save(clean)
    notify(task_id)
    return task_id
```

Use `normalize_title()` in Day 5's `create_task()` endpoint in your own refactor, mapping a `ValueError` to HTTP 422. For the exercise, keep the extracted function independently testable.

```bash
python -c 'from service import normalize_title; print(normalize_title("  Write   tests  "))'
git add service.py && git commit -m "refactor(day6): isolate task business logic and logging"
```


### Checkpoint — Locate the seam

**Run and inspect:** Trace which part of the function makes a business decision and which part sends a notification or writes a log.

**Code-review discussion:** Can you test the decision without the network or a full server process?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 2. Write focused tests with mocks

**Why mock the notifier?** Unit tests should not send real notifications. A mock lets you assert that a collaborator was called correctly and isolate failures in the function being tested. Do not mock every internal detail: also retain integration tests that prove real components work together.


**Read this file like a reviewer — `day06_quality/tests/test_service.py`:** Identify which collaborator gets mocked and which behavior remains real. Keep it in a separate editor tab as you run the example.

**`day06_quality/tests/test_service.py`**

```python
from unittest.mock import Mock
import pytest
from service import normalize_title, create_with_notifier


@pytest.mark.parametrize("raw,expected", [
    ("  Write   tests  ", "Write tests"),
    ("One task", "One task"),
])
def test_normalization(raw, expected):
    assert normalize_title(raw) == expected


def test_empty_title():
    with pytest.raises(ValueError):
        normalize_title("    ")


def test_save_and_notify():
    save = Mock(return_value=42)
    notify = Mock()
    assert create_with_notifier(" New task ", save, notify) == 42
    save.assert_called_once_with("New task")
    notify.assert_called_once_with(42)
```

```bash
python -m pytest -q tests/
python -m ruff check service.py tests/
python -m ruff format --check service.py tests/
# If formatting reports changes, run: python -m ruff format service.py tests/
git add tests/test_service.py && git commit -m "test(day6): add parametrized and mocked service tests"
```


### Checkpoint — Inspect mock assertions

**Run and inspect:** Change the expected notification deliberately; confirm a unit test detects the mismatch.

**Code-review discussion:** Do you still have a real end-to-end test, or have you mocked away every behavior?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 3. Automate checks in GitHub Actions

**Why run checks in CI?** A green test suite only on one laptop does not protect a shared branch. GitHub Actions can run formatting, linting, and tests on each push or pull request, helping catch missed checks before merging. Pin supported action versions and maintain your dependencies over time.


Create this file **from the repository root**: `.github/workflows/python.yml`.

**`.github/workflows/python.yml`**

```yaml
name: Python checks
on: [push, pull_request]
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: python -m pip install pytest "fastapi[standard]" httpx ruff
      - name: Run day tests
        run: |
          for dir in day01_expenses day02_library day03_logs day04_async day05_tasks day06_quality day07_capstone; do
            if [ -d "$dir/tests" ]; then
              (cd "$dir" && python -m pytest -q tests/) || exit 1
            fi
          done
      - name: Lint quality module
        run: python -m ruff check day06_quality/
```

```bash
cd ..
git add .github/workflows/python.yml
git diff --cached
git commit -m "ci(day6): run project tests and lint checks on push"
```

**Professional caveats:** Never hard-code secret tokens, never call external APIs from regular unit tests, and set up reusable database fixtures before testing parallel writes. The example CI workflow runs once the corresponding directories exist. On an actual project, pin action versions to trusted commit SHAs for stronger supply-chain control.

---


### Checkpoint — Validate CI locally

**Run and inspect:** Before pushing, run the exact test/lint commands configured in the workflow.

**Code-review discussion:** How will contributors know what a failed CI job means? Add failure-reproduction commands to README.

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 4 — Simulate a professional pull-request review

### 4.1 Run the full local quality gate

```bash
# From the relevant day project directory.
python -m pytest -q tests/
python -m ruff check .
python -m ruff format --check .
git diff --check
```

Not every repository starts fully formatted. If the formatter reports changes, review its proposed modifications and commit them deliberately rather than skipping the check.

### 4.2 Review what your tests actually cover

Map three kinds of evidence: pure function assertions, mocked collaborator interactions, and a real route/database workflow. Avoid claiming 100% correctness because all tests pass. Tests show behavior for the cases you wrote and the environment in which you ran them.

### 4.3 Write a useful pull-request description

A short professional PR explains *what* changed, *why* it changed, *how* you tested it, and *what remains risky*.

```markdown
## Summary
- Extracted task completion logic into a service.
- Added notification tests with a mock collaborator.
- Added automated lint and test checks.

## Verification
- [x] Unit tests
- [x] API integration tests (where applicable)
- [x] Ruff lint

## Known limitations
- Notification delivery is simulated in unit tests.
- Operational retry policy is not yet implemented.
```

### 4.4 CI failure drill

Temporarily introduce a lint error on a local branch; run Ruff and verify it catches the problem. Restore the file and rerun all checks before committing. **Do not push intentionally broken code to a shared main branch just to test CI.**

### 4.5 Know the boundary of mocks

A mocked notifier can prove that a service attempted to notify; it cannot prove that an external provider accepts the message. That requires a separate integration or contract test in an appropriate environment, with credentials handled securely.

### Day 6 independent challenges

- [ ] Parameterize a test with three inputs.
- [ ] Mock a collaborator that raises an exception.
- [ ] Explain whether the service should retry or propagate that exception.
- [ ] Add a README section showing all local checks.
- [ ] Check that secrets and `.env` files are ignored.
- [ ] Explain one drawback of testing only through mocks.

**Ready for Day 7 when:** You can run the project quality gate and describe which failures are caught by each test layer.

---


# Day 7 — Capstone: Job Application Tracker API

## Your mission and definition of done

**End product:** Bring models, persistence, HTTP, and testing together.

**Core review concepts:** foreign keys; schemas; referential integrity; CRUD endpoints; filters; status transitions; integration testing.

**Definition of done:** You should be able to walk a request from JSON validation to SQL and back, explain database relations, and demo an end-to-end application lifecycle.

**Scope boundary:** The minimal implementation is an educational prototype, not a production-ready authenticated service.

### How to approach every step

1. Read the rationale before opening the editor. Predict the shape of the input and output.
2. Create the named file exactly where the guide says, and enter the full code block.
3. Execute the smoke-test command, then deliberately try one invalid input.
4. Run tests where available, inspect `git status` and `git diff --cached`, and commit only the milestone's files.
5. Write down one design trade-off you would discuss during a code review.

**Commit convention:** `feat` for behavior, `test` for tests, `refactor` for restructuring without changed behavior, `docs` for documentation, and `chore` for tooling and setup. Hashes on your machine will naturally differ from another repository's.


**Learn:** multi-file architecture, validation, relational persistence, REST, filtering, tests, integration.


## Guided lab: design the lifecycle before implementing endpoints

Write down the intended business journey:

```text
Create Company
     ↓
Create Application for that Company
     ↓
List Applications by Status
     ↓
Move Application to Interview
     ↓
View Summary Statistics
```

Now map each arrow to an HTTP operation and a row or relationship in the database. The `company_id` field should refer to a real company: a foreign key is not merely a convenience—it records a valid relationship.

**Why validate status twice?** Request validation rejects unknown values before they reach the handler, while allowed status transitions can be a *business rule* depending on the current state. The minimal example validates allowed labels; it is not yet a complete state machine.

**Security review:** Do not publish this educational service with sensitive job-application notes exposed on a public URL. Production requires authentication, per-user authorization, secret management, and a deployment threat model.

**Professional acceptance test:** Exercise an entire workflow in one test with a temporary database, and verify not just success codes but saved data and summary counts.

## Step 1. Create a database and schemas

**Why split companies from applications?** A company can have multiple applications; a foreign key expresses that relationship without repeating company names everywhere. **Why enable SQLite foreign keys explicitly?** SQLite enforces foreign keys only when the connection has `PRAGMA foreign_keys = ON`. **Why use `Literal` for status?** The API can reject unsupported states such as `"maybe"` before saving inconsistent data.


```bash
mkdir -p day07_capstone/tests && cd day07_capstone
```

**Read this file like a reviewer — `day07_capstone/db.py`:** Identify where the database connection is created and closed and where schema initialization happens. Keep it in a separate editor tab as you run the example.

**`day07_capstone/db.py`**

```python
import sqlite3
import os


def connect():
    db = sqlite3.connect(os.environ.get("JOBS_DB", "jobs.db"))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'applied',
            FOREIGN KEY(company_id) REFERENCES companies(id)
        );
    """)
    return db
```

**Read this file like a reviewer — `day07_capstone/schemas.py`:** Distinguish fields callers may supply from values generated by the server. Keep it in a separate editor tab as you run the example.

**`day07_capstone/schemas.py`**

```python
from typing import Literal
from pydantic import BaseModel, Field

Status = Literal["applied", "interview", "offer", "rejected"]


class CompanyIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ApplicationIn(BaseModel):
    company_id: int = Field(gt=0)
    role: str = Field(min_length=1, max_length=150)
    status: Status = "applied"
```

```bash
python -c 'from schemas import ApplicationIn; print(ApplicationIn(company_id=1, role="Backend Engineer"))'
git add db.py schemas.py && git commit -m "feat(day7): model companies and job applications"
```


### Checkpoint — Verify relations

**Run and inspect:** Attempt creating an application with an absent company and inspect the expected behavior.

**Code-review discussion:** Is the foreign key constraint enabled for every SQLite connection?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 2. Implement API endpoints

**Why separate models, validation schemas, and routes?** Storage choices, input contracts, and HTTP handling evolve for different reasons. Keeping them distinct reduces the number of files affected by any one change. Database constraints are a second line of defense after API validation; do not rely on client-side checks alone.


**Read this file like a reviewer — `day07_capstone/app.py`:** Follow one handler from request validation through persistence to the response. Note which failures become HTTP errors. Keep it in a separate editor tab as you run the example.

**`day07_capstone/app.py`**

```python
import sqlite3
from fastapi import FastAPI, HTTPException, Query
from db import connect
from schemas import CompanyIn, ApplicationIn, Status

app = FastAPI(title="Job Application Tracker")


@app.post("/companies", status_code=201)
def create_company(body: CompanyIn):
    with connect() as db:
        try:
            cursor = db.execute("INSERT INTO companies(name) VALUES (?)", (body.name,))
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Company already exists")
        return {"id": cursor.lastrowid, "name": body.name}


@app.post("/applications", status_code=201)
def create_application(body: ApplicationIn):
    with connect() as db:
        try:
            cursor = db.execute(
                "INSERT INTO applications(company_id, role, status) VALUES (?, ?, ?)",
                (body.company_id, body.role, body.status),
            )
        except sqlite3.IntegrityError:
            raise HTTPException(404, "Company not found")
        return {"id": cursor.lastrowid, **body.model_dump()}


@app.get("/applications")
def list_applications(
    status: Status | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    query = """SELECT a.id, c.name AS company, a.role, a.status
               FROM applications a JOIN companies c ON c.id=a.company_id"""
    params = []
    if status:
        query += " WHERE a.status = ?"
        params.append(status)
    query += " ORDER BY a.id DESC LIMIT ? OFFSET ?"
    params += [limit, offset]
    with connect() as db:
        return [dict(row) for row in db.execute(query, params)]


@app.patch("/applications/{application_id}/status")
def change_status(application_id: int, status: Status):
    with connect() as db:
        cursor = db.execute("UPDATE applications SET status=? WHERE id=?",
                            (status, application_id))
        if cursor.rowcount == 0:
            raise HTTPException(404, "Application not found")
    return {"id": application_id, "status": status}


@app.get("/stats")
def stats():
    with connect() as db:
        rows = db.execute("SELECT status, COUNT(*) AS count FROM applications GROUP BY status")
        return {row["status"]: row["count"] for row in rows}
```

```bash
fastapi dev app.py
# Test endpoints in http://127.0.0.1:8000/docs; stop with Ctrl+C.
git add app.py && git commit -m "feat(day7): add application API, filtering, and statistics"
```


### Checkpoint — Trace a real request

**Run and inspect:** Send a request with valid fields, then one with a status outside the allowed values.

**Code-review discussion:** Does the HTTP response expose internal data that clients should never see?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 3. Add end-to-end API tests

**Why end-to-end API tests?** A unit test can prove a function works while the application still has broken routing, serialization, or SQL wiring. Tests that exercise HTTP requests through the application catch problems at the boundaries between layers. Keep the test database isolated from development data.


**Read this file like a reviewer — `day07_capstone/tests/test_capstone.py`:** Trace a multi-request workflow instead of testing only isolated endpoints. Keep it in a separate editor tab as you run the example.

**`day07_capstone/tests/test_capstone.py`**

```python
from fastapi.testclient import TestClient
from app import app


def test_application_workflow(tmp_path, monkeypatch):
    monkeypatch.setenv("JOBS_DB", str(tmp_path / "jobs.db"))
    client = TestClient(app)

    company = client.post("/companies", json={"name": "Example Co"})
    assert company.status_code == 201
    cid = company.json()["id"]

    application = client.post("/applications", json={
        "company_id": cid, "role": "Python Engineer", "status": "applied"
    })
    assert application.status_code == 201
    aid = application.json()["id"]

    assert len(client.get("/applications", params={"status": "applied"}).json()) == 1
    assert client.patch(f"/applications/{aid}/status", params={"status": "interview"}).status_code == 200
    assert client.get("/stats").json() == {"interview": 1}


def test_missing_company_and_invalid_status(tmp_path, monkeypatch):
    monkeypatch.setenv("JOBS_DB", str(tmp_path / "jobs.db"))
    client = TestClient(app)
    assert client.post("/applications", json={
        "company_id": 999, "role": "Engineer", "status": "applied"
    }).status_code == 404
    assert client.get("/applications", params={"status": "unknown"}).status_code == 422
```

```bash
python -m pytest -q tests/
git add tests/test_capstone.py && git commit -m "test(day7): verify application lifecycle and validation"
cd ..
```


### Checkpoint — Practice a full journey

**Run and inspect:** Create company → create application → list/filter → update status → read statistics. Repeat with a fresh temporary database.

**Code-review discussion:** What failed test would indicate that routing works but persistence is broken?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---

## Step 4. Finish and publish professionally

**Why document setup and verification?** A reviewer should be able to clone your repository, install requirements, run tests, and exercise the API without guessing. Before publishing, check `git status`, inspect staged changes, and ensure generated databases, secrets, and personal data are not tracked. A README is part of the project's usability, not an afterthought.


Add a root README explaining setup, the seven directories, how to run each project, and the most useful example commands. Include a screenshot of `/docs` **only if you personally captured it**. Then:

```bash
# From python-7-day-challenge/
(cd day07_capstone && python -m pytest -q tests/)
git status
git log --oneline --reverse
git diff --check
# Create an empty repository in your GitHub account first, then:
git remote add origin https://github.com/YOUR_USERNAME/python-7-day-challenge.git
git push -u origin main
```

**Capstone extension backlog:** interview events, per-user authentication/authorization, migrations, pagination metadata, secure secrets, Docker, CI, structured logging, more than ten tests, and deployment. These are **next steps**, not features implemented in the minimal example above.

---

## Step 5 — Capstone handoff and portfolio review

### 5.1 Follow a full API user story

Record the request, response, and stored data for this sequence:

1. Create a company.
2. Create an application tied to that company.
3. Fetch the application listing filtered by its status.
4. Update the application's status.
5. Fetch statistics and verify the updated count.

**Why test an entire story?** Isolated route tests can pass while the sequence fails because of inconsistent persistence or response models. An end-to-end API test checks the boundaries where modules meet.

### 5.2 Read your database design critically

Can a company have several applications? Can an application refer to a missing company? Are status values constrained? Are duplicates meaningful? The database and API should agree on these rules, because clients may be incorrect or malicious.

### 5.3 Document an honest release boundary

The minimal capstone deliberately omits features found in production services, including per-user authorization, migration tooling, robust audit logs, and hardened deployment settings. The README should call these out rather than presenting the demo as secure for public customer data.

### 5.4 Write a repeatable verification script

```bash
# Run from the day07_capstone directory
python -m pytest -q tests/
python -m compileall -q .
git status
git diff --check
```

If you publish to GitHub, keep the repository root free of `.db` files, secrets, and other environment-specific artifacts. Use a sample data set whose contents are invented, not copied from real job applications.

### 5.5 Reflect on architecture choices

Write a paragraph each on why you used SQL instead of JSON, why API schemas differ from database tables, which functions are unit-testable, and what you would add before accepting external users. These explanations turn a toy project into an interview-ready learning artifact.

### Capstone stretch backlog

- [ ] Add authenticated users and per-user data isolation.
- [ ] Add interview events with dates and notes.
- [ ] Add migration scripts for schema changes.
- [ ] Add status-transition rules with tests.
- [ ] Implement cursor-based pagination for large data sets.
- [ ] Add containerization and deployment instructions.

**Course complete when:** All projects run in a fresh environment, tests pass, each relevant change has a focused Git commit, and someone can reproduce the capstone from your README without personal guidance.

---


# Daily Professional Workflow Checklist

- [ ] Understand each function and input/output type.
- [ ] Implement code rather than only pasting it.
- [ ] Run the main demonstration.
- [ ] Run automated tests (`python -m pytest -q tests/` from that day's directory).
- [ ] Test one invalid input.
- [ ] Inspect `git status` and `git diff --cached`.
- [ ] Make a focused conventional commit.
- [ ] Update a README with setup and example commands.
- [ ] Note one refactoring opportunity for tomorrow.

# GitHub Reference Repositories

- Python fundamentals and exercises: https://github.com/realpython/materials
- Structured Python exercises: https://github.com/Asabeneh/30-Days-Of-Python
- Concepts and code examples: https://github.com/trekhleb/learn-python
- Algorithms and data structures: https://github.com/TheAlgorithms/Python
- Asynchronous HTTP client source: https://github.com/encode/httpx
- FastAPI full-stack reference: https://github.com/fastapi/full-stack-fastapi-template
- FastAPI engineering conventions: https://github.com/zhanymkanov/fastapi-best-practices
- pytest source and examples: https://github.com/pytest-dev/pytest
- Flask tutorial source (alternative web architecture): https://github.com/pallets/flask/tree/main/examples/tutorial

**How to study an open-source repo:** read `README.md`, run the documented example, trace one request/function from entry point to data layer, identify tests covering it, and recreate the feature yourself rather than copying its entire implementation.

# What you should be able to explain by the end

1. Why money is stored in integer cents rather than binary floats.
2. Why a data model shouldn't be responsible for printing CLI output.
3. Why generators are helpful for large files.
4. Why async improves many I/O-bound tasks but not CPU-bound code automatically.
5. How parameterized SQL queries mitigate SQL injection.
6. What an API validation error (422) means.
7. How mocked tests remain deterministic without network access.
8. Why Git commits should be small and meaningful.
9. How to separate schemas, persistence, business logic, and HTTP handlers.
10. Which parts of these tutorial projects require additional hardening before deployment.

## Engineering decisions at a glance

| Decision | Benefit | Boundary / alternative |
|---|---|---|
| Integer cents for expenses | Exact sums in a two-decimal currency | Multi-currency systems need currency-aware units |
| Temporary JSON then replace | Reduces incomplete writes | Does not solve concurrent writers; use locking/DB |
| Validation at boundaries | Fails early with useful errors | Domain/database constraints still matter |
| Separate CLI, domain, storage | Easier testing and replacement | Small scripts can reasonably be simpler |
| Dataclasses for entities | Less boilerplate | Behavior-heavy types may need regular classes |
| Generator-based log parsing | Bounded memory | Track malformed records and backpressure in production |
| Async HTTP with semaphore | Overlaps I/O, limits fan-out | CPU workloads need different strategies |
| Parameterized SQL | Prevents SQL injection via values | Identifier names still require safe allowlists |
| Mocked unit tests plus API tests | Fast feedback and integration confidence | Mocks alone can hide wiring problems |
| CI on pull requests | Repeatable quality checks | CI is not a substitute for code review |

### Checkpoint — Conduct a handoff review

**Run and inspect:** Have someone unfamiliar with the app follow the README from a fresh checkout. Record where they get stuck.

**Code-review discussion:** Which security features must be added before publishing this API on the public Internet?

**Before committing:** Run the command shown in this step, inspect `git status`, stage the relevant files, review `git diff --cached`, and make the named commit. If something fails, fix and rerun before moving forward.

---



# Professional Debugging & Git Review Recipes

## When the application fails

1. **Reproduce** the smallest input that fails, and record its exact command.
2. **Read** the full traceback or HTTP response body, including the first failing line in your code.
3. **Isolate** the layer: input validation, domain logic, persistence, HTTP, or test environment.
4. **Add a failing test** if the problem should stay fixed in future versions.
5. **Change one thing**, rerun the targeted test, and then the full suite.
6. **Review the diff** for unrelated changes before committing.

```bash
git status --short
git diff --check
git diff
git add path/to/changed_file.py
git diff --cached
git commit -m "fix: describe the observed bug"
git log --oneline -8
```

**Why stage specific files?** `git add .` is convenient, but it may scoop up generated databases, logs, local experiments, or credentials if `.gitignore` is incomplete. Review before commit and never add secrets.

## What counts as a professional commit?

A good commit has one logical goal, a meaningful subject, passing relevant tests, and no unrelated local artifacts. A test-only commit is fine when it proves existing behavior; if a feature and tests are tightly coupled, committing them together is often preferable to leaving a broken commit in history.

## Optional end-of-week oral review

Try answering without looking at the notes: How does one expense travel from a CLI argument into JSON? Who prevents two members from borrowing the same book? When does a generator run? Why do asynchronous functions need `await`? Which component guards against SQL injection? What does a mock prove versus an integration test? What does the database guarantee about a job application's company?


# 7-Day Python Intensive: From Review to Advanced

**Level:** Intermediate → Advanced  
**Duration:** 7 Days  
**Daily Commitment:** 4–6 hours  
**Approach:** Hands-on Projects + GitHub Source Code

## Learning Objectives

By the end of this intensive 7-day challenge, you will:

- Review Python fundamentals and problem-solving techniques.
- Understand object-oriented programming and clean code.
- Practice decorators, generators, iterators, and context managers.
- Work with algorithms, data structures, and asynchronous Python.
- Build REST APIs using FastAPI.
- Integrate SQL databases with Python.
- Write automated tests using pytest.
- Learn logging, profiling, debugging, and basic CI/CD.
- Build a portfolio-ready capstone project.

> **Note:** Seven days is an intensive learning sprint. It provides exposure to advanced techniques, but professional mastery requires continued practice.

---

## 7-Day Progress Tracker

- [ ] Day 1: Python Fundamentals — Expense Tracker CLI
- [ ] Day 2: Object-Oriented Programming — Library Management System
- [ ] Day 3: Advanced Python — Server Log Analyzer
- [ ] Day 4: Algorithms and Async Python — Async API Aggregator
- [ ] Day 5: Databases and REST APIs — Task Manager API
- [ ] Day 6: Testing and Optimization — Production-Quality API
- [ ] Day 7: Capstone — Job Application Tracker API

---

# Day 1 — Python Fundamentals

**Level:** Review  
**Duration:** 4–5 hours

## Topics

- Python variables and data types
- Lists, tuples, sets, and dictionaries
- Slicing
- List and dictionary comprehensions
- Functions and arguments
- Lambda functions
- Type hints
- Exception handling
- File handling
- JSON and CSV

## Coding Exercises

- [ ] Find duplicate values in a list.
- [ ] Count word frequencies using dictionaries.
- [ ] Sort employee records by salary.
- [ ] Read and summarize CSV data.
- [ ] Create functions with type hints.
- [ ] Handle invalid input using exceptions.

## Hands-on Project: Expense Tracker CLI

Build a command-line expense tracking application.

### Features

- Add new expenses.
- Categorize transactions.
- Calculate total spending.
- Summarize spending by category.
- Filter expenses by date.
- Save and load transactions from JSON.
- Export reports to CSV.

### Suggested Project Structure

    expense-tracker/
    ├── main.py
    ├── expense.py
    ├── storage.py
    ├── expenses.json
    ├── tests/
    └── README.md

### GitHub Repositories

1. [Real Python Materials](https://github.com/realpython/materials)
2. [30 Days of Python](https://github.com/Asabeneh/30-Days-Of-Python)
3. [Learn Python](https://github.com/trekhleb/learn-python)

### Completion Checklist

- [ ] Complete all exercises.
- [ ] Build a working CLI.
- [ ] Implement JSON persistence.
- [ ] Add basic input validation.
- [ ] Push source code to GitHub.

---

# Day 2 — Object-Oriented Programming and Clean Code

**Level:** Intermediate  
**Duration:** 4–5 hours

## Topics

- Classes and objects
- Constructors
- Instance and class attributes
- Encapsulation
- Inheritance
- Polymorphism
- Composition
- Properties
- Static methods
- Class methods
- Dataclasses
- Abstract base classes
- Custom exceptions
- SOLID principles

## Coding Exercises

- [ ] Implement a BankAccount class.
- [ ] Add deposit and withdrawal methods.
- [ ] Create account types using inheritance.
- [ ] Refactor a class using @dataclass.
- [ ] Implement abstract classes.
- [ ] Replace unnecessary inheritance with composition.

## Hands-on Project: Library Management System

Build a library management application using OOP.

### Suggested Classes

- Book
- Member
- Library
- Loan

### Features

- Add books.
- Register members.
- Borrow books.
- Return books.
- Search books.
- Check availability.
- Track active loans.
- Save and load records.

### Suggested Project Structure

    library-management/
    ├── main.py
    ├── models/
    │   ├── book.py
    │   ├── member.py
    │   └── loan.py
    ├── services/
    │   └── library.py
    ├── storage/
    ├── tests/
    └── README.md

### GitHub Repositories

1. [Real Python Materials](https://github.com/realpython/materials)
2. [Flask Tutorial Source](https://github.com/pallets/flask/tree/main/examples/tutorial)

### Completion Checklist

- [ ] Design domain models.
- [ ] Implement business logic.
- [ ] Add custom exceptions.
- [ ] Persist library records.
- [ ] Document project architecture.

---

# Day 3 — Advanced Python Features

**Level:** Advanced  
**Duration:** 5–6 hours

## Topics

- Decorators
- Closures
- Generators
- Iterators
- Context managers
- *args and **kwargs
- functools
- itertools
- collections
- Advanced type hints
- Lazy evaluation
- Functional programming techniques

## Coding Exercises

- [ ] Create an execution-time decorator.
- [ ] Implement a retry decorator.
- [ ] Write a generator for reading large files.
- [ ] Implement a custom context manager.
- [ ] Use functools.lru_cache.
- [ ] Use itertools for efficient iteration.

## Hands-on Project: Server Log Analyzer

Build a tool that analyzes server logs.

### Features

- Parse large log files.
- Count HTTP error codes.
- Identify frequently occurring IP addresses.
- Calculate request frequencies.
- Identify slow requests.
- Generate summary statistics.
- Export CSV and JSON reports.

### Advanced Challenge

Process very large files using generators without loading the entire file into memory.

### Suggested Project Structure

    log-analyzer/
    ├── main.py
    ├── parser.py
    ├── analyzer.py
    ├── decorators.py
    ├── reports.py
    ├── sample.log
    ├── tests/
    └── README.md

### GitHub Repositories

1. [Real Python Materials](https://github.com/realpython/materials)
2. [Learn Python](https://github.com/trekhleb/learn-python)

### Completion Checklist

- [ ] Implement at least one decorator.
- [ ] Use generators to process logs.
- [ ] Handle malformed log entries.
- [ ] Generate reports.
- [ ] Add automated tests.

---

# Day 4 — Algorithms, Data Structures, and Async Python

**Level:** Advanced  
**Duration:** 5–6 hours

## Topics

- Big-O time and space complexity
- Arrays and linked lists
- Stacks and queues
- Hash maps
- Trees and graphs
- Binary search
- Sorting algorithms
- Recursion
- asyncio
- async and await
- Threading
- Multiprocessing
- I/O-bound vs CPU-bound workloads

## Coding Exercises

- [ ] Implement binary search.
- [ ] Solve Two Sum.
- [ ] Solve Valid Parentheses.
- [ ] Implement an LRU cache.
- [ ] Write asynchronous HTTP requests.
- [ ] Compare sequential and concurrent execution.

## Hands-on Project: Async API Aggregator

Build a Python application that fetches and combines data from multiple public APIs.

### Features

- Fetch data from several API endpoints.
- Perform concurrent HTTP requests.
- Handle errors and timeouts.
- Normalize API responses.
- Save results in JSON.
- Benchmark execution times.
- Limit concurrency to avoid overwhelming APIs.

### Suggested Technologies

- asyncio
- httpx
- json
- time

### Suggested Project Structure

    async-api-aggregator/
    ├── main.py
    ├── api_client.py
    ├── aggregator.py
    ├── benchmark.py
    ├── tests/
    └── README.md

### GitHub Repositories

1. [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python)
2. [HTTPX Source Code](https://github.com/encode/httpx)

### Completion Checklist

- [ ] Solve at least five algorithm problems.
- [ ] Implement async HTTP requests.
- [ ] Handle timeouts.
- [ ] Benchmark performance.
- [ ] Document sequential vs concurrent results.

---

# Day 5 — Databases and REST API Development

**Level:** Advanced  
**Duration:** 5–6 hours

## Topics

- HTTP fundamentals
- REST API design
- FastAPI
- Pydantic
- Request and response validation
- SQL fundamentals
- SQLite
- PostgreSQL
- SQLModel or SQLAlchemy
- CRUD operations
- Dependency injection
- Pagination
- Filtering
- Error handling

## Coding Exercises

- [ ] Create a FastAPI application.
- [ ] Implement GET endpoints.
- [ ] Implement POST endpoints.
- [ ] Implement PUT and DELETE endpoints.
- [ ] Create database models.
- [ ] Add pagination and filtering.

## Hands-on Project: Task Manager REST API

Build a REST API for managing tasks.

### Features

- Create tasks.
- Update task details.
- Delete tasks.
- List all tasks.
- Filter tasks by status.
- Filter tasks by priority.
- Search tasks.
- Persist data in a database.
- Validate requests.
- Provide interactive API documentation.

### Example Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /tasks | List tasks |
| GET | /tasks/{id} | Get task |
| POST | /tasks | Create task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |
| GET | /tasks?status=done | Filter tasks |

### Suggested Project Structure

    task-manager/
    ├── app/
    │   ├── main.py
    │   ├── database.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── routes/
    │   └── services/
    ├── tests/
    ├── requirements.txt
    └── README.md

### GitHub Repositories

1. [Full Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)
2. [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
3. [Flask Tutorial](https://github.com/pallets/flask/tree/main/examples/tutorial)

### Completion Checklist

- [ ] Build CRUD endpoints.
- [ ] Integrate SQLite.
- [ ] Validate API payloads.
- [ ] Add pagination.
- [ ] Test the API using Swagger UI.

---

# Day 6 — Testing, Debugging, and Optimization

**Level:** Advanced  
**Duration:** 4–5 hours

## Topics

- pytest
- Test fixtures
- Parametrized tests
- Mocking
- Unit testing
- Integration testing
- Test coverage
- Logging
- pdb debugging
- cProfile
- Code formatting
- Ruff
- Environment configuration
- GitHub Actions

## Coding Exercises

- [ ] Write unit tests for API business logic.
- [ ] Create pytest fixtures.
- [ ] Mock external dependencies.
- [ ] Test invalid request payloads.
- [ ] Measure test coverage.
- [ ] Profile a slow function.
- [ ] Configure automated testing with GitHub Actions.

## Hands-on Project: Production-Quality Task Manager

Enhance the Day 5 Task Manager API.

### Features

- Automated unit and integration tests.
- Structured application logging.
- Centralized exception handling.
- Environment-based configuration.
- Ruff linting and formatting.
- GitHub Actions test workflow.
- Test coverage reporting.

### Suggested GitHub Actions Workflow

Create:

    .github/workflows/tests.yml

Example configuration:

    name: Python Tests

    on:
      push:
      pull_request:

    jobs:
      test:
        runs-on: ubuntu-latest

        steps:
          - uses: actions/checkout@v4

          - uses: actions/setup-python@v5
            with:
              python-version: "3.12"

          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt

          - name: Run tests
            run: pytest -v

### GitHub Repositories

1. [pytest](https://github.com/pytest-dev/pytest)
2. [Full Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)

### Completion Checklist

- [ ] Write automated tests.
- [ ] Add integration tests.
- [ ] Configure logging.
- [ ] Run a profiler.
- [ ] Configure CI with GitHub Actions.

---

# Day 7 — Advanced Capstone Project

**Level:** Advanced Integration  
**Duration:** 6 hours

## Project: Job Application Tracker API

Build a portfolio-ready backend application using advanced Python concepts.

## Core Features

- Manage job applications.
- Manage companies.
- Track interview events.
- Update application stages.
- Search applications.
- Filter by status.
- Sort by application date.
- Paginate results.
- Calculate application statistics.

## Required Technologies

- Python
- FastAPI
- Pydantic
- SQLModel or SQLAlchemy
- SQLite or PostgreSQL
- pytest
- Git
- GitHub

## Required Implementation Checklist

- [ ] Create database models.
- [ ] Implement REST endpoints.
- [ ] Add request validation.
- [ ] Implement business services.
- [ ] Handle application errors.
- [ ] Add filtering and pagination.
- [ ] Write at least 10 automated tests.
- [ ] Write API documentation.
- [ ] Publish source code on GitHub.

## Optional Advanced Challenges

- [ ] JWT authentication.
- [ ] Docker support.
- [ ] Database migrations using Alembic.
- [ ] GitHub Actions CI pipeline.
- [ ] Asynchronous background processing.
- [ ] Application deployment.

## Suggested Project Structure

    job-application-tracker/
    ├── app/
    │   ├── main.py
    │   ├── database.py
    │   ├── models/
    │   │   ├── application.py
    │   │   ├── company.py
    │   │   └── interview.py
    │   ├── schemas/
    │   ├── routes/
    │   ├── services/
    │   └── dependencies.py
    ├── tests/
    │   ├── test_applications.py
    │   ├── test_companies.py
    │   └── test_interviews.py
    ├── requirements.txt
    ├── Dockerfile
    ├── .gitignore
    └── README.md

## GitHub Repositories

1. [Full Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)
2. [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

---

# Complete GitHub Repository Reference

| GitHub Repository | Main Focus | Days |
|---|---|---|
| [Real Python Materials](https://github.com/realpython/materials) | Tutorials and example code | 1–3 |
| [30 Days of Python](https://github.com/Asabeneh/30-Days-Of-Python) | Python learning exercises | 1–3 |
| [Learn Python](https://github.com/trekhleb/learn-python) | Python code examples | 1–3 |
| [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) | Algorithms and data structures | 4 |
| [HTTPX](https://github.com/encode/httpx) | HTTP client and async examples | 4 |
| [FastAPI Full Stack Template](https://github.com/fastapi/full-stack-fastapi-template) | Production-oriented API source | 5–7 |
| [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) | FastAPI architecture guidance | 5–7 |
| [pytest](https://github.com/pytest-dev/pytest) | Testing framework source | 6 |
| [Flask Tutorial](https://github.com/pallets/flask/tree/main/examples/tutorial) | Example web application | 2, 5 |

> Some repositories contain runnable applications, while others provide individual examples, algorithms, tests, or architectural guidance.

---

# Daily Study Schedule

| Activity | Duration |
|---|---|
| Review concepts | 60 minutes |
| Solve coding exercises | 60 minutes |
| Build hands-on project | 120 minutes |
| Study GitHub source code | 30 minutes |
| Refactor, test, and document | 30 minutes |
| **Total** | **5 hours** |

---

# Development Environment Setup

Use Python 3.11+ and VS Code.

## Create Workspace

    mkdir python-7-day-challenge
    cd python-7-day-challenge

## Create Virtual Environment

    python -m venv .venv

## Activate Virtual Environment

macOS / Linux:

    source .venv/bin/activate

Windows PowerShell:

    .venv\Scripts\Activate.ps1

## Install Dependencies

    python -m pip install --upgrade pip
    python -m pip install pytest ruff httpx "fastapi[standard]" sqlmodel

---

# Recommended Workspace Structure

    python-7-day-challenge/
    ├── day01-expense-tracker/
    ├── day02-library-system/
    ├── day03-log-analyzer/
    ├── day04-async-api/
    ├── day05-task-manager/
    ├── day06-testing/
    ├── day07-capstone/
    └── README.md

---

# Day 1 Starter Coding Challenge

## Problem: Summarize Expenses

Given a list of expense records, calculate the total amount for each category.

## Example Code

    from collections import defaultdict

    def summarize_expenses(
        expenses: list[dict],
    ) -> dict[str, float]:
        totals = defaultdict(float)

        for expense in expenses:
            category = expense["category"]
            amount = float(expense["amount"])

            if amount < 0:
                raise ValueError("Negative expense")

            totals[category] += amount

        return dict(totals)


    expenses = [
        {"category": "food", "amount": 15},
        {"category": "travel", "amount": 40},
        {"category": "food", "amount": 25},
    ]

    print(summarize_expenses(expenses))

## Expected Output

    {"food": 40.0, "travel": 40.0}

## Extensions

- [ ] Read transactions from CSV.
- [ ] Group expenses by month.
- [ ] Find the highest spending category.
- [ ] Export reports to JSON.
- [ ] Add three or more pytest tests.

---

# Final Completion Checklist

- [ ] Completed all seven days.
- [ ] Built seven hands-on projects.
- [ ] Practiced advanced Python features.
- [ ] Solved algorithm challenges.
- [ ] Implemented asynchronous HTTP requests.
- [ ] Built a REST API.
- [ ] Integrated a SQL database.
- [ ] Created automated tests.
- [ ] Implemented basic CI/CD.
- [ ] Published projects on GitHub.
- [ ] Completed and documented the capstone.

---

# Recommended Learning Strategy

1. Read the concepts before starting implementation.
2. Attempt every exercise before looking at solutions.
3. Write the first version of each project yourself.
4. Study GitHub source code to learn patterns and architecture.
5. Refactor your implementation.
6. Write automated tests.
7. Commit your progress daily.
8. Document what you learned.

**Final Goal:** Build confidence with advanced Python concepts and complete a portfolio-ready backend application.
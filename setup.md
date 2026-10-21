# Professional Python Development Setup for VS Code

> A modern, clean, fast, and production-ready Python development environment using VS Code, uv, Ruff, Pyright, pytest, and Git.

## 1. Recommended Technology Stack

| Component | Tool | Purpose |
|---|---|---|
| Code Editor | VS Code | Python development |
| Python Version | Python 3.13 | Stable Python runtime |
| Package Manager | uv | Package and environment management |
| IntelliSense | Pylance | Autocomplete and code analysis |
| Linter | Ruff | Detect code quality issues |
| Formatter | Ruff | Automatic code formatting |
| Type Checker | Pyright | Static type checking |
| Testing | pytest | Unit and integration testing |
| Coverage | pytest-cov | Test coverage |
| Debugging | debugpy | Python debugger |
| Git Hooks | pre-commit | Automated code quality checks |
| Version Control | Git | Source control |

### Why this stack?

- Fast and lightweight
- Minimal overlapping tools
- Consistent coding standards
- Automatic formatting
- Strong type checking
- Reproducible environments
- Suitable for team development
- Ready for CI/CD integration

---

## 2. Install Required Software

### Install Python

Download Python:

https://www.python.org/downloads/

Recommended version: Python 3.13.

Verify:

```bash
python --version
```

### Install VS Code

Download:

https://code.visualstudio.com/

### Install Git

Download:

https://git-scm.com/downloads

Verify:

```bash
git --version
```

### Install uv

Official installation guide:

https://docs.astral.sh/uv/getting-started/installation/

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify:

```bash
uv --version
```

---

## 3. Essential VS Code Extensions

Install these extensions through VS Code's Extensions panel.

| Extension | Extension ID | Purpose |
|---|---|---|
| Python | `ms-python.python` | Python development support |
| Pylance | `ms-python.vscode-pylance` | IntelliSense and type analysis |
| Python Debugger | `ms-python.debugpy` | Debugging |
| Python Environments | `ms-python.vscode-python-envs` | Environment management |
| Ruff | `charliermarsh.ruff` | Linting and formatting |
| GitLens | `eamodio.gitlens` | Git history and insights |
| Error Lens | `usernamehw.errorlens` | Inline errors and warnings |
| Jupyter | `ms-toolsai.jupyter` | Notebook support (optional) |

Install extensions from the terminal:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension ms-python.vscode-python-envs
code --install-extension charliermarsh.ruff
code --install-extension eamodio.gitlens
code --install-extension usernamehw.errorlens
```

**Note:** The Python extension may automatically install some Microsoft extensions as dependencies.

---

## 4. Create a Python Project

Initialize a package-based project:

```bash
uv init --package my-project
cd my-project
```

Install and select Python:

```bash
uv python install 3.13
uv python pin 3.13
```

Install development dependencies:

```bash
uv add --dev ruff pytest pytest-cov pyright pre-commit
```

Synchronize the environment:

```bash
uv sync
```

Open VS Code:

```bash
code .
```

### Select Python Interpreter

1. Open the VS Code Command Palette.
2. Search for `Python: Select Interpreter`.
3. Select the interpreter inside `.venv`.

The environment location is typically:

Windows:

```text
.venv\Scripts\python.exe
```

macOS / Linux:

```text
.venv/bin/python
```

**Important:** Prefer using `uv run` for project commands. It automatically uses the correct environment.

---

## 5. Professional Project Structure

```text
my-project/
│
├── .vscode/
│   ├── settings.json
│   └── launch.json
│
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── main.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

### Directory Responsibilities

| Directory/File | Responsibility |
|---|---|
| `.vscode/` | Editor configuration |
| `src/` | Application source code |
| `tests/` | Automated tests |
| `pyproject.toml` | Project and tool configuration |
| `uv.lock` | Dependency lockfile |
| `.python-version` | Python version selection |
| `.pre-commit-config.yaml` | Git quality checks |
| `.gitignore` | Git exclusions |

Do not commit `.venv/` to Git.

---

## 6. VS Code Settings

Create:

```text
.vscode/settings.json
```

Configuration:

```json
{
  "editor.formatOnSave": true,
  "editor.formatOnPaste": true,
  "editor.rulers": [88],
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.detectIndentation": true,

  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,

  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },

  "python.defaultInterpreterPath": "${workspaceFolder}/.venv",
  "python.analysis.typeCheckingMode": "standard",
  "python.analysis.diagnosticMode": "workspace",

  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": ["tests"],

  "editor.minimap.enabled": false,
  "editor.bracketPairColorization.enabled": true,

  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/.ruff_cache": true
  }
}
```

### Features Enabled

- Automatic formatting when saving
- Automatic import sorting and supported fixes
- Type error diagnostics
- pytest integration
- Consistent indentation
- Trailing whitespace removal
- Cleaner file explorer

---

## 7. Configure Ruff

Ruff handles:

- Linting
- Code formatting
- Import sorting
- Unused import detection
- Common coding mistakes
- Code modernization

Add the following configuration to `pyproject.toml`.

**Important:** Keep the existing `[project]` and `[build-system]` sections generated by uv.

```toml
[tool.ruff]
target-version = "py313"
line-length = 88
src = ["src"]

[tool.ruff.lint]
select = [
    "E4",
    "E7",
    "E9",
    "F",
    "I",
    "B",
    "UP",
    "SIM",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Ruff Commands

Check code:

```bash
uv run ruff check .
```

Automatically fix issues:

```bash
uv run ruff check --fix .
```

Format code:

```bash
uv run ruff format .
```

Check formatting without making changes:

```bash
uv run ruff format --check .
```

---

## 8. Configure Static Type Checking

Use Pyright for static type checking.

Add to `pyproject.toml`:

```toml
[tool.pyright]
include = ["src", "tests"]
typeCheckingMode = "standard"
pythonVersion = "3.13"
```

Run:

```bash
uv run pyright
```

### Type Checking Levels

| Mode | Description |
|---|---|
| off | Minimal checking |
| basic | Basic type checking |
| standard | Balanced type checking |
| strict | Strong type safety |

Recommended:

- Personal projects: `standard`
- Professional team projects: `standard`
- Strictly typed libraries: `strict`

Example:

```python
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity
```

Using type annotations improves code readability, autocomplete, and static analysis.

---

## 9. Configure pytest

Add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"

[tool.coverage.run]
branch = true
source = ["my_project"]

[tool.coverage.report]
show_missing = true
fail_under = 80
```

Example production code in `src/my_project/main.py`:

```python
def add(a: int, b: int) -> int:
    return a + b
```

Example test in `tests/test_main.py`:

```python
from my_project.main import add


def test_add() -> None:
    assert add(2, 3) == 5
```

Run tests:

```bash
uv run pytest
```

Run coverage:

```bash
uv run pytest --cov=my_project --cov-report=term-missing
```

Recommended coverage target: 80% or higher for codebases where that threshold is appropriate.

**Note:** High coverage does not guarantee high-quality tests.

---

## 10. Configure VS Code Debugging

Create:

```text
.vscode/launch.json
```

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: Project Module",
      "type": "debugpy",
      "request": "launch",
      "module": "my_project.main",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
```

### Debugging Shortcuts

| Shortcut | Action |
|---|---|
| F5 | Start debugging |
| F9 | Toggle breakpoint |
| F10 | Step over |
| F11 | Step into |
| Shift + F11 | Step out |
| Shift + F5 | Stop debugging |

---

## 11. Configure Git Hooks

Git hooks help prevent poor-quality code from being committed.

Create:

```text
.pre-commit-config.yaml
```

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.0
    hooks:
      - id: ruff-check
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: pyright
        name: pyright
        entry: uv run pyright
        language: system
        pass_filenames: false
```

The Ruff tag above is an example version; select a verified release appropriate for your project.

Install hooks:

```bash
uv run pre-commit install
```

Run all hooks:

```bash
uv run pre-commit run --all-files
```

The hooks automatically run during normal Git commits.

---

## 12. Gitignore Configuration

Create `.gitignore`:

```gitignore
# Python environments
.venv/
venv/
env/

# Python cache
__pycache__/
*.py[cod]

# Testing
.pytest_cache/
.coverage
.coverage.*
htmlcov/

# Ruff
.ruff_cache/

# Pyright
.pyright/

# Build artifacts
build/
dist/
*.egg-info/

# Environment variables and secrets
.env
.env.*
!.env.example

# Operating system
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/
```

### Git Best Practices

- Commit `pyproject.toml`
- Commit `uv.lock`
- Commit `.python-version`
- Commit project-specific `.vscode/` configuration
- Never commit `.venv/`
- Never commit secrets or actual `.env` files

---

## 13. Dependency Management with uv

Add a production dependency:

```bash
uv add requests
```

Add a development dependency:

```bash
uv add --dev pytest
```

Remove a dependency:

```bash
uv remove requests
```

Synchronize dependencies:

```bash
uv sync
```

Run a Python module:

```bash
uv run python -m my_project.main
```

Run a Python script:

```bash
uv run python script.py
```

Update dependencies within configured version constraints:

```bash
uv lock --upgrade
uv sync
```

### Why uv?

- Fast dependency resolution
- Automated virtual environment management
- Lockfile support
- Reproducible installations
- Python version management
- Simplified project commands

---

## 14. Daily Development Commands

| Task | Command |
|---|---|
| Install dependencies | `uv sync` |
| Add package | `uv add requests` |
| Add dev package | `uv add --dev pytest` |
| Run Python | `uv run python` |
| Run application | `uv run python -m my_project.main` |
| Format code | `uv run ruff format .` |
| Check lint | `uv run ruff check .` |
| Fix lint | `uv run ruff check --fix .` |
| Check formatting | `uv run ruff format --check .` |
| Type checking | `uv run pyright` |
| Run tests | `uv run pytest` |
| Test coverage | `uv run pytest --cov=my_project` |
| Git quality checks | `uv run pre-commit run --all-files` |

---

## 15. Professional Development Workflow

### Step 1: Write Code

Use:

- Pylance autocomplete
- Python type hints
- Clear naming conventions
- Small, focused functions
- Meaningful documentation

### Step 2: Save Files

VS Code automatically:

- Formats Python code
- Organizes imports
- Applies supported Ruff fixes
- Displays remaining diagnostics

### Step 3: Validate Code

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

### Step 4: Run Tests

```bash
uv run pytest
```

### Step 5: Run Coverage

```bash
uv run pytest --cov=my_project --cov-report=term-missing
```

### Step 6: Commit Changes

```bash
git add .
git commit -m "feat: implement new feature"
```

Pre-commit hooks validate the staged changes.

### Step 7: Push Changes

```bash
git push
```

For team projects, run the same checks in CI before merging.

---

## 16. Recommended Coding Standards

### Follow PEP 8

Use:

- Four spaces per indentation level
- Descriptive variable names
- Consistent formatting
- Small functions and modules
- Clear imports

### Use Type Hints

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

### Use Meaningful Names

Avoid:

```python
def calc(x, y):
    return x * y
```

Prefer:

```python
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity
```

### Avoid Bare Exceptions

Avoid:

```python
try:
    process_data()
except:
    pass
```

Prefer:

```python
try:
    process_data()
except ValueError as exc:
    logger.exception("Failed to process data")
    raise
```

### Prefer Structured Logging

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Application started")
```

Use logging rather than `print()` for operational messages in production applications.

---

## 17. Optional Advanced Tools

| Tool | Use Case |
|---|---|
| GitHub Actions | Continuous integration |
| Docker | Containerized development |
| Dependabot / Renovate | Dependency updates |
| Bandit | Python security analysis |
| pip-audit | Dependency vulnerability checks |
| MkDocs | Documentation |
| FastAPI | Backend API development |
| SQLAlchemy | Database interaction |
| Jupyter | Interactive data analysis |

Only add tools that solve a genuine project need.

---

## 18. Setup Verification Checklist

### Environment

- [ ] Python installed
- [ ] VS Code installed
- [ ] Git installed
- [ ] uv installed
- [ ] `.venv` created
- [ ] Correct Python interpreter selected

### VS Code

- [ ] Python extension installed
- [ ] Pylance enabled
- [ ] Ruff installed
- [ ] Format on save enabled
- [ ] Type checking enabled
- [ ] pytest discovery working
- [ ] Debugger working

### Project Quality

- [ ] `pyproject.toml` configured
- [ ] Ruff configured
- [ ] Pyright configured
- [ ] pytest configured
- [ ] Tests passing
- [ ] pre-commit installed
- [ ] `.gitignore` configured
- [ ] `uv.lock` committed

---

## 19. Final Recommended Stack

**Core**

```text
VS Code
    +
Python 3.13
    +
uv
    +
Pylance
    +
Ruff
    +
Pyright
    +
pytest
    +
pre-commit
    +
Git
```

**Development process**

```text
Write Code
    ↓
Autocomplete + Type Diagnostics
    ↓
Save
    ↓
Ruff Format + Lint
    ↓
Pyright Type Checking
    ↓
pytest Tests
    ↓
pre-commit Checks
    ↓
Git Commit
    ↓
CI/CD
```

## 20. Official References

- VS Code Python: https://code.visualstudio.com/docs/languages/python
- Python Documentation: https://docs.python.org/3/
- uv: https://docs.astral.sh/uv/
- Ruff: https://docs.astral.sh/ruff/
- Pyright: https://github.com/microsoft/pyright
- pytest: https://docs.pytest.org/
- pre-commit: https://pre-commit.com/
- Git: https://git-scm.com/doc

---

**Recommended default:** VS Code + Python 3.13 + uv + Ruff + Pylance + Pyright + pytest + pre-commit.

This combination provides a lightweight, maintainable, and production-oriented Python development environment without requiring a large collection of overlapping tools.
"""Read and write expense records using JSON."""

import json
import os

from pathlib import Path
from tempfile import NamedTemporaryFile

"""
Why use a temporary file?
A simple implementation might use open("expenses.json", "w"), but that could leave an incomplete file if writing fails.
Our implementation first writes to a temporary file and then replaces the destination using os.replace(). On a typical local filesystem, this helps avoid partially written JSON files.
It doesn't provide full transaction durability or protect against multiple processes writing concurrently; those are later-stage concerns.
"""

def load_expenses(path: Path) -> list[dict]:
    if not path.exists():
        return []

    try:
        data = json.loads(
            path.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}"
        ) from exc

    if not isinstance(data, list):
        raise TypeError(
            "Expenses file must contain a JSON list"
        )

    return data

def save_expenses(
        path: Path,
        expenses: list[dict],
) -> None:
    """Save JSON through a temporary file to avoid partial writes."""

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_path = None

    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=".expenses-",
            suffix=".tmp",
            delete=False,
        ) as file:
            temp_path = Path(file.name)

            json.dump(
                expenses,
                file,
                indent=2,
            )

            file.write("\n")
        os.replace(temp_path, path)

    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
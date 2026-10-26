"""Filtering, summaries, and CSV export."""

import csv

from collections import defaultdict
from datetime import date
from pathlib import Path

from expense import format_money

def filter_month(
        expenses: list[dict],
        month: str | None,
) -> list[dict]:
    if month is None:
        return expenses

    try:
        date.fromisoformat(f"{month}-01")
    except ValueError as exc:
        raise ValueError(
            "Month must be YYYY-MM"
        ) from exc

    if len(month) != 7:
        raise ValueError("Month must be YYYY-MM")

    return [
        expense
        for expense in expenses
        if expense["date"].startswith(month + "-")
    ]

def total_by_category(expenses: list[dict]) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)

    for expense in expenses:
        totals[expense["category"]] += expense["amount_cents"]

    return dict(sorted(totals.items()))

def export_csv(
        path: Path,
        expenses: list[dict],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "date",
            "category",
            "amount",
            "note",
        ])

        for expense in expenses:
            writer.writerow([
                expense["date"],
                expense["category"],
                format_money(expense["amount_cents"]),
                expense["note"],
            ])


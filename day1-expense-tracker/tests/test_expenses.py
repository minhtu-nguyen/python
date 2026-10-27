import csv
import tempfile
import unittest

from pathlib import Path

from expense import make_expense, parse_amount
from main import main
from reports import (
    export_csv,
    filter_month,
    total_by_category,
)
from storage import load_expenses, save_expenses

class ExpenseTests(unittest.TestCase):
    def test_cents_are_exact(self):
        self.assertEqual(parse_amount("0.10"), 10)
        self.assertEqual(parse_amount("12.50"), 1250)

    def test_reject_invalid_amounts(self):
        invalid = ["-1", "0", "NaN", "abc", "1.234"]

        for amount in invalid:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    parse_amount(amount)

    def test_normalize_category(self):
        expense = make_expense(
            "2.50",
            " food ",
            " lunch ",
            "2026-10-21",
        )

        self.assertEqual(expense["category"], "food")
        self.assertEqual(expense["note"], "lunch")

    def test_reject_bad_date(self):
        with self.assertRaises(ValueError):
            make_expense(
                "2.00",
                "food",
                when="2026-02-30",
            )

    def test_storage_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "expenses.csv"

            data = [
                make_expense(
                    "7.00",
                    "travel",
                    when="2026-10-21",
                )
            ]

            save_expenses(path, data)
            loaded = load_expenses(path)

            self.assertEqual(loaded, data)

    def test_bad_json(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "brokenjson"
            path.write_text(
                "not json",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_expenses(path)

    def test_month_filter_and_totals(self):
        expenses = [
            make_expense(
                "2.50",
                "food",
                when="2026-10-20",
            ),
            make_expense(
                "1.25",
                "food",
                when="2026-10-21",
            ),
            make_expense(
                "4.00",
                "travel",
                when="2026-09-01"
            )
        ]

        october = filter_month(
            expenses,
            "2026-10",
        )

        self.assertEqual(
            total_by_category(october),
            {"food": 375}
        )

        self.assertEqual(
            len(filter_month(expenses, None)),
            3,
        )

        with self.assertRaises(ValueError):
            filter_month(expenses, "2026-99")

    def test_csv_expoert(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "report.csv"

            expenses = [
                make_expense(
                    "3.25",
                    "food",
                    "snack",
                    "2026-10-21"
                )
            ]

            export_csv(path, expenses)

            with path.open(
                newline="",
                encoding="utf-8"
            ) as file:
                rows = list(csv.DictReader(file))

            self.assertEqual(
                rows[0]["amount"],
                "3.25"
            )

    def test_cli_add_and_read(self):
        with tempfile.TemporaryDirectory() as td:
            path = str(Path(td) / "expenses.json")

            result = main([
                "--file", path,
                "add",
                "--amount", "10",
                "--category", "food",
                "--date", "2026-10-21",
            ])

            self.assertEqual(result, 0)

            loaded = load_expenses(Path(path))

            self.assertEqual(
                loaded[0]["amount_cents"],
                1000
            )

if __name__ == "__main__":
    unittest.main()
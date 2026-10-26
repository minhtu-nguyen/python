"""Command-line interface for the expense tracker."""

import argparse
from pathlib import Path

from expense import format_money, make_expense
from reports import (
    export_csv,
    filter_month,
    total_by_category,
)

from storage import load_expenses, save_expenses

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track daily expenses")

    parser.add_argument(
        "--file",
        type=Path,
        default=Path("expenses.json"),
        help="Json data file",
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # Add a new expense
    add = sub.add_parser(
        "add",
        help="Add an expense",
    )
    add.add_argument("--amount", required=True)
    add.add_argument("--category", required=True)
    add.add_argument("--note", default="")
    add.add_argument("--date", help="YYYY-MM-DD")

    # List expenses
    listing = sub.add_parser(
        "list",
        help="List expenses",
    )
    listing.add_argument("--month")

    # Summarize spending
    summary = sub.add_parser(
        "summary",
        help="Sum by category",
    )
    summary.add_argument("--month")

    # Export a CSV report
    export = sub.add_parser(
        "export",
        help="Export records to CSV",
    )
    export.add_argument(
        "--output",
        type=Path,
        required=True,
    )
    export.add_argument("--month")

    return parser

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        expenses = load_expenses(args.file)

        if args.command == "add":
            record = make_expense(
                args.amount,
                args.category,
                args.note,
                args.date,
            )

            expenses.append(record)
            save_expenses(args.file, expenses)

            print(
                f"Added {record['category']}: "
                f"{format_money(record['amount_cents'])}"
            )
        elif args.command == "list":
            selected = filter_month(expenses, args.month)

            for expense in selected:
                print(
                    f"{expense['date']} | "
                    f"{expense['category']:12} | "
                    f"{format_money(expense['amount_cents']):>8} | "
                    f"{expense['note']}"
                )

        elif args.command == "summary":
            selected = filter_month(expenses, args.month)

            totals = total_by_category(selected)

            for category, cents in totals.items():
                print(
                    f"{category:12} "
                    f"{format_money(cents):>8}"
                )

            total = sum(
                expense["amount_cents"]
                for expense in selected
            )

            print(
                f"TOTAL: {format_money(total):>8}"
            )

        elif args.command == "export":
            selected = filter_month(
                expenses,
                args.month,
            )

            export_csv(
                args.output,
                selected,
            )

            print(
                f"Exported {len(selected)} expenses "
                f"to {args.output}"
            )

        return 0

    except (ValueError, OSError) as exc:
        parser.exit(
            2,
            f"Error: {exc}\n"
        )

if __name__ == "__main__":
    raise SystemExit(main())
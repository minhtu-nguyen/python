"""Input validation and creation of expense records."""

from datetime import date
from decimal import Decimal, InvalidOperation

def parse_amount(amount: str) -> int:
    """Convert a positive amount into integer cents."""

    try:
        value = Decimal(amount)
    except InvalidOperation as exc:
        raise ValueError("Amount must be a number.") from exc

    if not value.is_finite() or value <= 0:
        raise ValueError("Amount must be a positive, finite number.")

    if value.as_tuple().exponent < -2:
        raise ValueError("Amount can have at most 2 decimal places")

    return int(value * 100)

def make_expense(amount: str, category: str, note: str = "", when: str | None = None) -> dict:
    """Create a validated, JSON-compatible expense."""
    category = category.strip()

    if not category:
        raise ValueError("Category must not be empty")

    day = date.fromisoformat(when) if when else date.today()

    return {
        "date": day.isoformat(),
        "category": category,
        "amount_cents": parse_amount(amount),
        "note": note.strip()
    }

def format_money(cents: int) -> str:
    """
    Notice that we store amount_cents as an integer rather than 12.50 as a floating-point number.
    This is an important engineering decision: binary floating-point calculations can produce rounding problems when dealing with money.
    """
    return f"{cents / 100:.2f}"

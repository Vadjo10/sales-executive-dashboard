from __future__ import annotations

import re
from typing import Any


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, str(email)))


def validate_phone(phone: str) -> bool:
    cleaned = re.sub(r"[\s\-\(\)]", "", str(phone))
    return len(cleaned) >= 8 and cleaned.isdigit()


def validate_price(price: float) -> bool:
    return isinstance(price, (int, float)) and price >= 0


def validate_quantity(quantity: int) -> bool:
    return isinstance(quantity, int) and quantity > 0


def validate_non_empty(value: Any) -> bool:
    return value is not None and (not isinstance(value, (str, list, dict)) or len(value) > 0)

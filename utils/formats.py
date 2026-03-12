# utils/formats.py
from babel.numbers import format_currency, format_percent


def fmt_currency(value: float, currency: str = "USD", locale: str = "pt_BR") -> str:
    return format_currency(value or 0.0, currency, locale=locale)


def fmt_percent(value: float, locale: str = "pt_BR", fmt: str = "#,##0.00%") -> str:
    return format_percent(value or 0.0, locale=locale, format=fmt)

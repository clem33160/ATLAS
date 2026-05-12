from __future__ import annotations

from decimal import Decimal, getcontext

getcontext().prec = 80


def scientific_notation(value: int) -> str:
    if value == 0:
        return "0"
    exponent = len(str(abs(value))) - 1
    mantissa = Decimal(value) / (Decimal(10) ** exponent)
    return f"{mantissa.normalize()}e{exponent}"


def human_readable_count(value: int) -> str:
    units = [(10**30, "nonillion"), (10**24, "septillion"), (10**21, "sextillion"), (10**18, "quintillion"), (10**15, "quadrillion"), (10**12, "trillion"), (10**9, "billion"), (10**6, "million")]
    for threshold, label in units:
        if value >= threshold:
            ratio = Decimal(value) / Decimal(threshold)
            return f"{ratio.quantize(Decimal('0.01'))} {label}"
    return f"{value}"

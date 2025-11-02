
from decimal import Decimal, ROUND_HALF_UP

def kg_to_lb(kg) -> Decimal:
    return (kg * Decimal("2.20462")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def kg_to_oz(kg) -> Decimal:
    return (kg * Decimal("35.274")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def cm_to_in(cm) -> Decimal:
    return (cm / Decimal("2.54")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
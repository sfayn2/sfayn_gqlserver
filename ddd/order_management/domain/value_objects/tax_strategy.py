from __future__ import annotations
import pytz
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional, List, Dict, Union
from datetime import datetime
from ddd.order_management.domain import enums, exceptions
from .coupon import Coupon

@dataclass(frozen=True) 
class TaxStrategy:
    tax_type: enums.TaxType
    inclusive: bool
    conditions: dict
    is_active: bool
    rate: Optional[Decimal] = None


    def __post_init__(self):
        if not self.conditions.get("country"):
            raise exceptions.InvalidOrderOperation(f'{self.tax_type.value} tax requires a "country" in conditions. eg. {"country": "singapore"}')

        if self.tax_type == enums.TaxType.GST:
            if self.rate is None or self.rate <= Decimal("0"):
                raise exceptions.InvalidOrderOperation("GST tax requires a valid non-zero rate")
        elif self.tax_type == enums.TaxType.STATE_TAX:
            if not self.conditions.get("state_tax_rate"):
                raise exceptions.InvalidOrderOperation('STATE_TAX requires a "state_tax_rate" in conditions. eg. {"state_tax_rate": {"CA": 0.075, "TX": 0.07 } }')

            state_rates = self.conditions.get("state_tax_rate")
            if not isinstance(state_rates, dict) or not state_rates:
                raise exceptions.InvalidOrderOperation(f'{self.tax_type.value} must be a non-empty dict.')
            
            for state, rate in state_rates.items():
                if not isinstance(state, str) or not state.strip():
                    raise exceptions.InvalidOrderOperation(f'Invalid state key in conditions: {state}')

                if not isinstance(rate, Decimal) or rate <= Decimal("0"):
                    raise exceptions.InvalidOrderOperation(f'Invalid tax rate for state {state}: {rate}')

            if self.rate is not None:
                raise exceptions.InvalidOrderOperation(f'{self.tax_type.value} should not define a global rate.')




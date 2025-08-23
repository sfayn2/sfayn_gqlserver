from __future__ import annotations
from typing import List, Dict, Tuple, Optional
from decimal import Decimal

from ddd.order_management.domain import (
    repositories,
    models,
    exceptions,
    value_objects
    )


class TaxService:

    def __init__(self, tax_options: List[tax_strategies.ports.TaxStrategyAbstract]):
        self.tax_options = tax_options

    def calculate_all_taxes(
        self, 
        order: models.Order, 
        vendor_tax_options: List[dtos.VendorTaxOptionSnapshotDTO]
    ) -> Tuple[value_objects.Money, List[str]]:
        valid_taxes = []

        # tax options to handler 
        for vendor_option in vendor_tax_options: #source alwys assumed its active
            key = (vendor_option.tax_type, vendor_option.provider.lower())
            strategy_factories = self.tax_options.get(key, [])
            for factory in strategy_factories:
                strategy_ins = factory(
                    vendor_option.tenant_id, 
                    vendor_option
                )
                valid_taxes.append(strategy_ins)


        tax_amount = value_objects.Money.default()
        tax_results = []
        options = []

        for option in valid_taxes:
            if option.is_eligible(order):
                res = option.calculate_tax(order)
                if res:
                    tax_results.append(res)


        return tax_results



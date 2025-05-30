from typing import List, Dict, Tuple, Optional
from decimal import Decimal

from ddd.order_management.domain import (
    repositories,
    models,
    exceptions,
    value_objects
    )

from ddd.order_management.domain.services.tax_strategies import (
    ports,
    singapore_tax,
    us_tax
)

DEFAULT_TAX_STRATEGIES = [
    singapore_tax.SingaporeTaxStrategy(),
    us_tax.USStateTaxStrategy()
]

class TaxStrategyService(ports.TaxStrategyServiceAbstract):

    def calculate_all_taxes(self, order: models.Order, tax_strategies: List[ports.TaxStrategyAbstract] = DEFAULT_TAX_STRATEGIES) -> Tuple[value_objects.Money, List[str]]:
        tax_amount = value_objects.Money.default()
        tax_results = []

        for tax_strategy in tax_strategies:
            res = tax_strategy.calculate_tax(order)
            if res:
                tax_results.append(res)
                #tax_details.append(tax_results.desc)
                #tax_amount = tax_amount.add(tax_results.amount)

        #return tax_amount.format(), tax_details
        return tax_results

            


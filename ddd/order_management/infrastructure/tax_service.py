import requests
from dataclasses import dataclass
from ddd.order_management.domain.services import tax_calculation_policies

@dataclass
class TaxService:
    def get_tax_calculation(country):
        if country.lower() == "singapore":
            return tax_calculation_policies.SGTaxCalculationPolicy()
        elif country.lower() == "united states":
            return tax_calculation_policies.USTaxCalculationPolicy()
        else:
            return ValueError(f"Tax calculation for {country} not supported.")

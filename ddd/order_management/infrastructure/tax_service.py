import requests
from dataclasses import dataclass
from ddd.order_management.domain.services import tax_calculation_policies
from ddd.order_management.domain import models

@dataclass
class TaxService:
    def __init__(self, tax_calculation_factory: tax_calculation_policies.TaxCalculationPolicyFactory):
        self.tax_calculation_factory = tax_calculation_factory

    def get_tax_policy(self, country: str):
        return self.tax_calculation_factory.get_tax_policy(country)

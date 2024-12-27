import requests
from dataclasses import dataclass
from ddd.order_management.domain.services import tax_service

@dataclass
class ExternalApiTaxService(tax_service.TaxService):
    api_url: str
    api_key: str

    def fetch_tax_rate(self, category, location):
        response = requests.get(
            f"{self.api_url}/tax_rates",
            headers={"Authorization": f"Bearer {self.api_key}"},
            params={"category": category, "location": location}
        )

        if response.status_code == 200:
            return response.json().get("rate", 0.0)
        return 0.0

    #location -> destination
    def calculate_tax(self, product, quantity, customer=None, location=None):
        if not product.is_taxable:
            return 0.0

        #if customer.is_tax_exempt:
        #    return 0.0

        tax_rate = self.fetch_tax_rate(product.category, location)
        total_price = product.price*quantity
        return round(total_price * tax_rate, 2)




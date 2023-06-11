
from ....ordering_domain import abstract_domain_models

class Address(abstract_domain_models.ValueObject):
    street: str
    city: str
    state: str
    country: str
    zipcode: str
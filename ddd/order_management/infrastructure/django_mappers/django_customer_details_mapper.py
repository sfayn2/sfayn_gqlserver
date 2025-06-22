import ast
from ddd.order_management.domain import models, value_objects

class CustomerDetailsMapper:

    @staticmethod
    def to_domain(customer_object) -> value_objects.CustomerDetails:
        return value_objects.CustomerDetails(
            customer_id=customer_object.customer_id,
            first_name=customer_object.customer_first_name,
            last_name=customer_object.customer_last_name,
            email=customer_object.customer_email
        )
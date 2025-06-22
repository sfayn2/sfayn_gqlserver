import ast
from ddd.order_management.domain import models, value_objects

class AddressMapper:

    @staticmethod
    def to_domain(customer_address) -> value_objects.Address:
        return value_objects.Address(
            street=customer_address.street,
            city=customer_address.city,
            state=customer_address.state,
            postal=int(customer_address.postal_code),
            country=customer_address.country
        )
        #return value_objects.Address(
        #    street=django_order_object.delivery_street,
        #    city=django_order_object.delivery_city,
        #    postal=int(django_order_object.delivery_postal),
        #    country=django_order_object.delivery_country,
        #    state=django_order_object.delivery_state
        #)
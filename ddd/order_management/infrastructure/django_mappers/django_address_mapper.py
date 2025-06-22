import ast
from ddd.order_management.domain import models, value_objects
from order_management import models as django_address_models

class AddressMapper:

    @staticmethod
    def to_domain(django_address_object) -> value_objects.Address:
        if hasattr(django_address_object, "delivery_street"):
            django_address_object.street = django_address_object.delivery_street
            django_address_object.city = django_address_object.delivery_city
            django_address_object.postal = django_address_object.delivery_postal
            django_address_object.country = django_address_object.delivery_country
            django_address_object.state = django_address_object.delivery_state

        return value_objects.Address(
            street=django_address_object.street,
            city=django_address_object.city,
            state=django_address_object.state,
            postal=int(django_address_object.postal),
            country=django_address_object.country
        )
        #return value_objects.Address(
        #    street=django_order_object.delivery_street,
        #    city=django_order_object.delivery_city,
        #    postal=int(django_order_object.delivery_postal),
        #    country=django_order_object.delivery_country,
        #    state=django_order_object.delivery_state
        #)
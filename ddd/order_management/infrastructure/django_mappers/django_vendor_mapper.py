import ast
from ddd.order_management.domain import models, value_objects
from vendor_management import models as django_vendor_models

class VendorDetailsMapper:

    @staticmethod
    def to_domain(django_vendor_details) -> value_objects.VendorDetails:
        return value_objects.VendorDetails(
            id=django_vendor_details.values_list("id", flat=True)[0],
            name=django_vendor_details.values_list("name", flat=True)[0],
            country=django_vendor_details.values_list("country", flat=True)[0]
        )
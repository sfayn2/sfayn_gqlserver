from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects

class VendorDetailsMapper:
    @staticmethod
    def to_domain(vendor_details_dto: dtos.VendorDetailsDTO) -> value_objects.VendorDetails:
        return value_objects.VendorDetails(
                id=vendor_details_dto.id, 
                name="TBD", 
                country="TBD"
            )
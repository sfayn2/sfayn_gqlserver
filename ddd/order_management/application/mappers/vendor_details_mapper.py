from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects

class VendorDetailsMapper:
    @staticmethod
    def to_domain(vendor_details_dto: dtos.VendorDetailsDTO) -> value_objects.VendorDetails:
        return value_objects.VendorDetails(
                vendor_id=vendor_details_dto.vendor_id, 
                name="TBD", 
                country="TBD"
            )
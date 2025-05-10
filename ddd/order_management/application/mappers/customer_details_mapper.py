from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects

class CustomerDetailsMapper:

    @staticmethod
    def to_domain(custom_details_dto: dtos.CustomerDetailsDTO) -> value_objects.CustomerDetails:
        return value_objects.CustomerDetails(**custom_details_dto.model_dump())
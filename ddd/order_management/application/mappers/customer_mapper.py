from dataclasses import asdict
from ddd.order_management.application import dtos
from ddd.order_management.domain import models, value_objects, enums

class CustomerDetailsMapper:

    @staticmethod
    def to_domain(dto: dtos.CustomerDetailsRequestDTO) -> value_objects.CustomerDetails:
        return value_objects.CustomerDetails(**dto.model_dump())

    @staticmethod
    def to_domain_from_response(dto: dtos.CustomerDetailsResponseDTO) -> value_objects.CustomerDetails:
        return value_objects.CustomerDetails(**dto.model_dump())

    @staticmethod
    def to_response_dto(customer_details: value_objects.CustomerDetails) -> dtos.CustomerDetailsResponseDTO:
        return dtos.CustomerDetailsResponseDTO(**asdict(customer_details))

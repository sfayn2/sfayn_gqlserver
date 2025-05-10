from ddd.order_management.application import dtos
from ddd.order_management.domain import value_objects

class PackageMapper:

    @staticmethod
    def to_domain(package_dto: dtos.PackageDTO) -> value_objects.Package:
        return value_objects.Package(**package_dto.model_dump())
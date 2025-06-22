from __future__ import annotations
from abc import ABC, abstractmethod

# ========
# Validate customer address
# ==========
class CustomerAddressValidationServiceAbstract(ABC):

    #TODO what if gues?
    @abstractmethod
    def ensure_customer_address_is_valid(
        self, customer_id: str, address: dtos.AddressDTO
    ) -> value_objects.Address:
        raise NotImplementedError("Subclasses must implement this method")
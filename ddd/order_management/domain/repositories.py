import uuid
from abc import ABC, abstractmethod

class VendorRepository(ABC):

    @abstractmethod
    def get_offers(self):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get_shipping_options(self):
        raise NotImplementedError("Subclasses must implement this method")

class PaymentGatewayRepository(ABC):

    @abstractmethod
    def get_payment_details(self):
        raise NotImplementedError("Subclasses must implement this method")


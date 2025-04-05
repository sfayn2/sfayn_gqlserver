from abc import ABC, abstractmethod

class PaymentGatewayAbstract(ABC):

    @abstractmethod
    def get_payment_details(self):
        raise NotImplementedError("Subclasses must implement this method")


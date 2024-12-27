from abc import ABC, abstractmethod

class TaxService(ABC):
    def calculate_tax(self, product, quantity, customer=None, location=None):
        raise NotImplementedError("Subclasses must implement this method")
import uuid
from abc import ABC, abstractmethod
from ddd.product_catalog.domain import models

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: models.Product):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get(self, product_id: uuid.uuid4) -> models.Product:
        raise NotImplementedError("Subclasses must implement this method")

class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: models.Category):
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def get(self, category_id: uuid.uuid4) -> models.Category:
        raise NotImplementedError("Subclasses must implement this method")
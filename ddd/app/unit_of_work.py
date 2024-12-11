from abc import ABC, abstractmethod
from typing import TypeVar
from django.db import transaction
from domain import repositories
from infrastructure import django_repository

T = TypeVar("T")

class AbstractUnitOfWork(ABC):
    product_catalog: repositories.ProductCatalogRepository

    def __enter__(self) -> T:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class DjangoUnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        self.product_catalog = django_repository.DjangoProductRepository
        transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        transaction.set_autocommit(True)

    def commit(self):
        transaction.commit()

    def rollback(self):
        transaction.rollback()
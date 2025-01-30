from abc import ABC, abstractmethod
from typing import TypeVar
from django.db import transaction
from ddd.product_catalog.domain import repositories
from ddd.product_catalog.infrastructure import django_repository

T = TypeVar("T")

class AbstractUnitOfWork(ABC):
    product: repositories.ProductRepository
    category: repositories.CategoryRepository

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


class DjangoOrderUnitOfWork(AbstractUnitOfWork):
    #make sure to call uow within block statement
    #to trigger this
    def __enter__(self):
        self.product = django_repository.DjangoProductRepository()
        self.category = django_repository.DjangoCategoryRepository()

        self.atomic = transaction.atomic()
        self.atomic.__enter__()
        return super().__enter__()

    def __exit__(self, *args):

        self.atomic.__exit__(*args)
        super().__exit__(*args)

    def commit(self):
        #do nothing since transaction.atomic() auto handle it
        pass

    def rollback(self):
        self.atomic.__exit__(Exception, Exception(), None)
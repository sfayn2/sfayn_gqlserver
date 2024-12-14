from abc import ABC, abstractmethod
from typing import TypeVar
from django.db import transaction
from ddd.product_catalog.domain import repositories
from ddd.product_catalog.infrastructure import django_repository

T = TypeVar("T")

class AbstractUnitOfWork(ABC):
    product: repositories.ProductRepository

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
    #make sure to call uow within block statement
    #to trigger this
    def __enter__(self):
        self.product = django_repository.DjangoProductRepository()
        self.atomic = transaction.atomic()
        self.atomic.__enter__()
        #transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):

        self.atomic.__exit__(*args)
        super().__exit__(*args)
        #transaction.set_autocommit(True)

    def commit(self):
        pass
        #transaction.commit()

    def rollback(self):
        self.atomic.__exit__(Exception, Exception(), None)
        #transaction.rollback()
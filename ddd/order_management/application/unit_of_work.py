from abc import ABC, abstractmethod
from typing import TypeVar
from django.db import transaction
from ddd.order_management.domain import repositories
from ddd.order_management.infrastructure import (
    django_customer_repository, 
    django_order_repository, 
    django_vendor_repository, 
    paypal_gateway_repository
)

T = TypeVar("T")

class AbstractUnitOfWork(ABC):
    order: repositories.OrderRepository
    vendor: repositories.VendorRepository
    customer: repositories.CustomerRepository
    payment_gateway: repositories.PaymentGatewayRepository

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
    def __init__(self):
        self.order = django_order_repository.DjangoOrderRepository()
        self.customer = django_customer_repository.DjangoCustomerRepository()
        self.vendor = django_vendor_repository.DjangoVendorRepository()
        #self.payment_gateway = paypal_gateway_repository.PaypalPaymentGatewayRepository()

    def __enter__(self):

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
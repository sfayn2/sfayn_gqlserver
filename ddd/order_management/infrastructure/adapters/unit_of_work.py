from abc import ABC, abstractmethod
from django.db import transaction
from ddd.order_management.infrastructure.adapters import (
    django_customer_repository, 
    django_order_repository, 
    django_vendor_repository,
)
from ddd.order_management.infrastructure import event_bus
from ddd.order_management.domain import repositories

class DjangoOrderUnitOfWork(repositories.UnitOfWorkAbstract):
    #make sure to call uow within block statement
    #to trigger this
    def __init__(self):
        self.order = django_order_repository.DjangoOrderRepositoryImpl()
        self.customer = django_customer_repository.DjangoCustomerRepositoryImpl()
        self.vendor = django_vendor_repository.DjangoVendorRepositoryImpl()

        self.event_publisher = event_bus
        self._events = []

    def __enter__(self):

        self.atomic = transaction.atomic()
        self.atomic.__enter__()
        return super().__enter__()

    def __exit__(self, *args):

        self.atomic.__exit__(*args)
        super().__exit__(*args)

    def commit(self):
        #do nothing since transaction.atomic() auto handle it
        self._collect_events()
        self._publish_events()

    def rollback(self):
        self.atomic.__exit__(Exception, Exception(), None)

    def _collect_events(self):
        self._events = []

        for entity in self.order.seen:
            if hasattr(entity, "_events"):
                self._events.extend(entity._events) #append not override
                entity._events.clear() #prevent duplicate processing

    def _publish_events(self):
        for event in self._events:
            print(f"Publish event : {event}")
            self.event_publisher.publish(event, self)


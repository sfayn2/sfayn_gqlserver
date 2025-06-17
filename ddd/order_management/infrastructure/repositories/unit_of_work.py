from abc import ABC, abstractmethod
from django.db import transaction
from ddd.order_management.infrastructure import django_mappers, event_bus, repositories as impl_repositories
from ddd.order_management.domain import repositories

class DjangoOrderUnitOfWork(repositories.UnitOfWorkAbstract):
    #make sure to call uow within block statement
    #to trigger this
    def __init__(self):
        self.order = impl_repositories.DjangoOrderRepositoryImpl()
        self.customer = impl_repositories.DjangoCustomerRepositoryImpl()
        self.vendor = impl_repositories.DjangoVendorRepositoryImpl()

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
        self.publish_events()

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
            self.event_publisher.publish(event)
    
    def publish_events(self):
        self._collect_events()
        self._publish_events()


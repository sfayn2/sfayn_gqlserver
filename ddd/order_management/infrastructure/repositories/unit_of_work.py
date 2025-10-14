from abc import ABC, abstractmethod
from django.db import transaction
from ddd.order_management.infrastructure import django_mappers, event_bus, repositories as impl_repositories, user_action
from ddd.order_management.domain import repositories

class DjangoOrderUnitOfWork(repositories.UnitOfWorkAbstract):
    #make sure to call uow within block statement
    #to trigger this
    def __init__(self):
        self.order = impl_repositories.DjangoOrderRepositoryImpl()
        self.user_action = user_action.DjangoUserActionRepository()

        self.event_publisher = event_bus


        self._events = []

    def __enter__(self):
        self.atomic = transaction.atomic()
        self.atomic.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.atomic.__exit__(exc_type, exc_val, exc_tb)

    def commit(self):
        while True:
            self._collect_events()
            if not self._events:
                break
            self._publish_events()

    def rollback(self):
        #can be used manually if needed
        self.atomic.__exit__(Exception, Exception(), None)

    def _collect_events(self):
        self._events = []

        for entity in self.order.seen:
            if hasattr(entity, "_events"):
                self._events.extend(entity._events) #append not override

        #prevent duplicate proces
        self.order.seen.clear()


    def _publish_events(self):
        for event in self._events:
            print(f"Publish event : {event}")
            self.event_publisher.publish(event, self)

    


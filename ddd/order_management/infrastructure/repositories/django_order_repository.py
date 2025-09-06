from ddd.order_management.domain import models, repositories, exceptions
from order_management import models as django_models
from ddd.order_management.infrastructure import django_mappers

#ok to return Domain for repository
class DjangoOrderRepositoryImpl(repositories.OrderAbstract):
    def get(self, order_id: str, tenant_id: str) -> models.Order:
        django_order = django_models.Order.objects.get(order_id=order_id, tenant_id=tenant_id)
        order_domain = django_mappers.OrderMapper.to_domain(django_order)
        self.seen.add(order_domain) #Track Entitry for Uow
        return order_domain
    
    def save(self, order: models.Order): 
        django_order = django_mappers.OrderMapper.to_django(order)
        obj, created = django_models.Order.objects.update_or_create(**django_order)

        for line_item in order.line_items:
            django_line_item = django_mappers.LineItemMapper.to_django(order.order_id, line_item)
            django_models.OrderLine.objects.update_or_create(**django_line_item)

        for act in order.activities:
            django_order_activity = django_mappers.OrderActivityMapper.to_django(order.order_id, act)
            django_models.OrderActivities.objects.update_or_create(**django_order_activity)

        self.seen.add(order) #Track Entitry for Uow

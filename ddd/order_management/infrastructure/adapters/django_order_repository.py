from ddd.order_management.domain import models, repositories, exceptions
from order_management import models as django_models
from ddd.order_management.infrastructure import infra_mappers
from ddd.order_management.application import mappers as application_mappers

#ok to return Domain for repository
class DjangoOrderRepositoryImpl(repositories.OrderAbstract):
    def get(self, order_id) -> models.Order:
        django_order = django_models.Order.objects.get(order_id=order_id)
        order_dto = infra_mappers.OrderMapper.to_dto(django_order)
        order_domain = application_mappers.OrderMapper.to_domain(order_dto)
        self.seen.append(order_domain) #Track Entitry for Uow
        return order_domain
    
    def save(self, order: models.Order): 
        django_order = infra_mappers.OrderMapper.to_django(order)
        _, created = django_models.Order.objects.update_or_create(**django_order)

        for line_item in order.line_items:
            django_line_item = infra_mappers.LineItemMapper.to_django(order.order_id, line_item)
            django_models.OrderLine.objects.update_or_create(**django_line_item)

        self.seen.append(order) #Track Entitry for Uow

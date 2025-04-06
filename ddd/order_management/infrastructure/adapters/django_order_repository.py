from ddd.order_management.domain import repositories, models, exceptions
from order_management import models as django_models
from ddd.order_management.infrastructure import order_dtos

class DjangoOrderRepositoryImpl(repositories.OrderAbstract):
    def get(self, order_id):
        django_order = django_models.Order.objects.get(order_id=order_id)
        order = order_dtos.OrderDTO.from_django_model(django_order).to_domain()
        self.seen.append(order) #Track Entitry for Uow
        return order
    
    def save(self, order: models.Order): 
        order_dto = order_dtos.OrderDTO.from_domain(order)
        django_order, created = django_models.Order.objects.update_or_create(**order_dto.to_django())

        for line_item in order.line_items:
            line_item_dto = order_dtos.LineItemDTO.from_domain(line_item)
            django_models.OrderLine.objects.update_or_create(**line_item_dto.to_django(order))

        self.seen.append(order) #Track Entitry for Uow

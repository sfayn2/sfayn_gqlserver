from ddd.order_management.domain import repositories, models, exceptions
from order_management import models as django_models
from ddd.order_management.infrastructure import infra_mappers, order_dtos
from ddd.order_management.application import dtos

class DjangoOrderRepositoryImpl(repositories.OrderAbstract):
    def get(self, order_id):
        django_order = django_models.Order.objects.get(order_id=order_id)
        order_dto = infra_mappers.OrderMapper.from_django_model(django_order)
        self.seen.append(order_dto) #Track Entitry for Uow
        return order_dto
    
    def save(self, order_dto: dtos.OrderDTO): 
        django_order = infra_mappers.OrderMapper.to_django(order_dto)
        _, created = django_models.Order.objects.update_or_create(**django_order)

        for line_item in order_dto.line_items:
            django_line_item = infra_mappers.LineItemMapper.to_django(order_dto.order_id, line_item)
            django_models.OrderLine.objects.update_or_create(**django_line_item)

        self.seen.append(order_dto) #Track Entitry for Uow

from ddd.order_management.domain import repositories, models
from order_management import models as django_models
from ddd.order_management.infrastructure import dtos

class DjangoOrderRepository(repositories.OrderRepository):
    def get(self, order_id):
        order = django_models.Order.objects.get(order_id=order_id)
        order_dto = dtos.OrderDTO.from_django_model(order)
        return order_dto.to_domain()
    
    def save(self, order: models.Order): 
        order_dto = dtos.OrderDTO.from_domain(order)
        order_dict = {
            "order_id": order.order_id,
            "defaults": order_dto.to_django_defaults()
        }
        django_order, created = django_models.Order.objects.update_or_create(**order_dict)

        for line_item in order.line_items:
            line_item_dto = dtos.LineItemDTO.from_domain(line_item)
            line_item_dict = {
                "product_sku": line_item.product_sku,
                "defaults": line_item_dto.to_django_defaults(order)
            }
            django_models.OrderLine.update_or_create(**line_item_dict)

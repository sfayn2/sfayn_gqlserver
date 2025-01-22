from ddd.order_management.domain import repositories, models
from order_management import models as django_models
from ddd.order_management.infrastructure import dtos

class DjangoOrderRepository(repositories.OrderRepository):
    def get(self, order_id):
        order = django_models.Order.objects.get(id=order_id)
        return dtos.OrderDTO(**order.to_dict()).to_domain()
    
    def save(self, order: models.Order): 
        order_dict = {
            "order_id": order.order_id,
            "defaults": dtos.OrderDTO(**order.__dict__).to_django_defaults()
        }
        django_models.Order.objects.update_or_create(**order_dict)

        for line_item in order.line_items:
            default_dict = dtos.LineItemDTO(**line_item.__dict__).dict().update({"order_id": order.order_id})
            line_item_dict = {
                "product_sku": line_item.product_sku,
                "defaults": default_dict
            }
            django_models.OrderLine.update_or_create(**line_item_dict)

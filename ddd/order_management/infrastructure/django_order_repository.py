from ddd.order_management.domain import repositories, models
from order_management import models as django_models

class DjangoOrderRepository(repositories.OrderRepository):
    def get(self, order_id):
        order = django_models.Order.objects.get(id=order_id)
        return order.to_domain()
    
    def save(self, order: models.Order): 
        import pdb;pdb.set_trace()
        order_model = django_models.Order.from_domain(order)
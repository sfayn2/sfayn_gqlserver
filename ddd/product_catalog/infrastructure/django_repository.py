from ddd.product_catalog.domain import repositories, models, enums
from ddd.product_catalog.infrastructure import vendor_policy
from product_catalog import models as django_models

class DjangoProductRepository(repositories.ProductRepository):
    def get(self, product_id):
        vendor_policy = vendor_policy.get_policy(product_id)
        product = django_models.Product.objects.get(id=product_id).to_domain(
            vendor_policy
            )
        return product
    
    def save(self, product: models.Product): 
        product_model = django_models.Product.from_domain(product)


class DjangoCategoryRepository(repositories.CategoryRepository):
    def get(self, category_id):
        category = django_models.Category.objects.get(id=category_id).to_domain()
        return category
    
    def save(self, category: models.Category): 
        category_model = django_models.Category.from_domain(category)
from ddd.product_catalog.domain import repositories, models
from product_catalog import models as django_models

class DjangoProductRepository(repositories.ProductRepository):
    def get(self, product_id):
        product_model = django_models.Product.objects.get(id=product_id)
        variants = [
            models.VariantItem(
                _variant_item_id=variant.id,
                _sku=variant.sku,
                _name=variant.name,
                _options=variant.options,
                _price=variant.price,
                _default=variant.default,
                _is_active=variant.is_active,
                _tags=list(variant.prodvariant2tag.values_list('name', flat=True))
            )
            for variant in product_model.product2variantitem.all()
        ]

        product = models.ProductCatalog(
            _id=product_model.id,
            _name=product_model.name,
            _description=product_model.description,
            _status=product_model.status,
            _variant_items=variants,
            _category=product_model.category.id
        )

        return product


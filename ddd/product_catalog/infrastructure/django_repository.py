from ddd.product_catalog.domain import repositories, models, enums
from product_catalog import models as django_models


class DjangoProductRepository(repositories.ProductRepository):
    def get(self, product_id):
        product_model = django_models.Product.objects.get(id=product_id)
        variants = [
            models.VariantItem(
                _id=variant.id,
                _sku=variant.sku,
                _name=variant.name,
                _options=variant.options,
                _price=variant.price,
                _stock=variant.stock,
                _default=variant.default,
                _is_active=variant.is_active,
                _tags=list(variant.prodvariant2tag.values_list('name', flat=True))
            )
            for variant in product_model.product2variantitem.all()
        ]

        product = models.Product(
            _id=product_model.id,
            _name=product_model.name,
            _description=product_model.description,
            _status=product_model.status,
            _variant_items=variants,
            _category=product_model.category.id,
            _created_by=product_model.created_by, 
            _date_created=product_model.date_created, 
            _date_modified=product_model.date_modified
        ) 
        
        
        return product 
    
    def save(self, product: models.Product): 
        product_model = django_models.Product.objects.update_or_create( id=product._id, defaults={ "name": product._name,
                "description": product.get_desc(),
                "category_id": product.get_category(),
                "status": product.get_status(),
                "created_by": product.get_created_by(),
                "date_created": product.get_date_created(),
                "date_modified": product.get_date_modified()
            }
        )
        #TODO create to_domain, from_domain
        for variant in product.get_variant_items():
            variant_model = django_models.VariantItem.objects.update_or_create(
                id=variant.get_id(),
                defaults={
                    "sku": variant.get_sku(),
                    "name": variant.get_name(),
                    "options": variant.get_options(),
                    "price": variant.get_price(),
                    "stock": variant.get_stock(),
                    "default": variant.get_default(),
                    "is_active": variant.is_active(),
                }

            )



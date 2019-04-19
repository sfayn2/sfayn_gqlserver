import graphene

from graphene_django.types import DjangoObjectType

from .models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(object):
    all_products = graphene.List(ProductType)

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

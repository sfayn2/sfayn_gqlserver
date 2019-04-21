import graphene

from graphene_django.types import DjangoObjectType

from .models import Product, ProductWarehouse, ProductOriginalImg, ProductDescImg

class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class ProductWarehouseType(DjangoObjectType):
    class Meta:
        model = ProductWarehouse


class ProductOriginalImgType(DjangoObjectType):
    class Meta:
        model = ProductOriginalImg


class ProductDescImgType(DjangoObjectType):
    class Meta:
        model = ProductDescImg


class Query(object):
    all_products = graphene.List(ProductType)
    all_warehouses = graphene.List(ProductWarehouseType)
    all_originalimgs = graphene.List(ProductOriginalImgType)
    all_descimgs = graphene.List(ProductDescImgType)

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_all_warehouses(self, info, **kwargs):
        return ProductWarehouse.objects.select_related('product').all()

    def resolve_all_originalimgs(self, info, **kwargs):
        return ProductOriginalImg.objects.select_related('product').all()
    
    def resolve_all_descimgs(self, info, **kwargs):
        return ProductDescImg.objects.select_related('product').all()
    

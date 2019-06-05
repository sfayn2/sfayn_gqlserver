import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Product, ProductWarehouse, ProductOriginalImg, ProductDescImg, ProductParent, ProductCategory

class ProductParentNode(DjangoObjectType):
    class Meta:
        model = ProductParent
        filter_fields = {
                'parent_sn': ['exact', 'icontains', 'istartswith'],
                } 
        interfaces = (relay.Node,)

class ProductCategoryNode(DjangoObjectType):
    class Meta:
        model = ProductCategory
        filter_fields = ("cat_name",)
        interfaces = (relay.Node,)


class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = {"title": ["exact", "icontains", "istartswith"], 
                         "sku": ["exact"],
                         "cat__cat_name": ["exact", "icontains"]
                         }
        interfaces = (relay.Node,)


class ProductWarehouseNode(DjangoObjectType):
    class Meta:
        model = ProductWarehouse
        filter_fields = ("warehouse",)
        interfaces = (relay.Node,)


class ProductOriginalImgNode(DjangoObjectType):
    class Meta:
        model = ProductOriginalImg
        filter_fields = ("original_img",)
        interfaces = (relay.Node,)


class ProductDescImgNode(DjangoObjectType):
    class Meta:
        model = ProductDescImg
        filter_fields = ("desc_img",)
        interfaces = (relay.Node,)


class Query(object):
    productparent = relay.Node.Field(ProductParentNode)
    all_productparents = DjangoFilterConnectionField(ProductParentNode)

    productcategory = relay.Node.Field(ProductCategoryNode)
    all_productcategory = DjangoFilterConnectionField(ProductCategoryNode)
    
    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)

    warehouse = relay.Node.Field(ProductWarehouseNode)
    all_warehouses = DjangoFilterConnectionField(ProductWarehouseNode)

    original_img = relay.Node.Field(ProductOriginalImgNode)
    all_original_imgs = DjangoFilterConnectionField(ProductOriginalImgNode)

    desc_img = relay.Node.Field(ProductDescImgNode)
    all_desc_imgs = DjangoFilterConnectionField(ProductDescImgNode)

#class ProductType(DjangoObjectType):
#    class Meta:
#        model = Product
#
#
#class ProductWarehouseType(DjangoObjectType):
#    class Meta:
#        model = ProductWarehouse
#
#
#class ProductOriginalImgType(DjangoObjectType):
#    class Meta:
#        model = ProductOriginalImg
#
#
#class ProductDescImgType(DjangoObjectType):
#    class Meta:
#        model = ProductDescImg
#
#
#class Query(object):
#    all_products = graphene.List(ProductType, 
#                                 title=graphene.String(),
#                                 sku=graphene.Int())
#    all_warehouses = graphene.List(ProductWarehouseType)
#    all_originalimgs = graphene.List(ProductOriginalImgType)
#    all_descimgs = graphene.List(ProductDescImgType)
#
#
#    def resolve_all_products(self, info, **kwargs):
#        title = kwargs.get("title")
#        sku = kwargs.get("sku")
#
#        if title is not None:
#            return Product.objects.filter(title__contains=title)
#
#        if sku is not None:
#            return Product.objects.get(sku=sku)
#        return Product.objects.all()
#
#    def resolve_all_warehouses(self, info, **kwargs):
#        return ProductWarehouse.objects.select_related('product').all()
#
#    def resolve_all_originalimgs(self, info, **kwargs):
#        return ProductOriginalImg.objects.select_related('product').all()
#    
#    def resolve_all_descimgs(self, info, **kwargs):
#        return ProductDescImg.objects.select_related('product').all()
#    

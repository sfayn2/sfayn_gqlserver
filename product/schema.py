
import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from django.db.models import Sum, F, FloatField
from .models import (
    ProductParent,
    ProductVariant,
    ProductVideo,
    ProductImage,
    ProductCategory
)


class ProductParentNode(DjangoObjectType):
    class Meta:
        model = ProductParent
        filter_fields = {
                'parent_sn': ['exact', 'icontains', 'istartswith'],
                } 
        interfaces = (relay.Node,)


class ProductCategoryNode(DjangoObjectType):
    level = graphene.String()
    class Meta:
        model = ProductCategory
        interfaces = (relay.Node,)
        filter_fields = ("name", "level")

    def resolve_level(self, info):
        return self.get_level_display()


class ProductVariantNode(DjangoObjectType):
    class Meta:
        model = ProductVariant
        interfaces = (relay.Node,)
        filter_fields = {
            "sku": ["exact"],
        }


class ProductImageNode(DjangoObjectType):
    class Meta:
        model = ProductImage
        interfaces = (relay.Node,)
        filter_fields = ("img_url",)
        

class ProductVideoNode(DjangoObjectType):
    class Meta:
        model = ProductVideo
        interfaces = (relay.Node,)
        filter_fields = ("video_url",)


class ProductVariantNode(DjangoObjectType):
    class Meta:
        model = ProductVariant
        interfaces = (relay.Node,)
        filter_fields = ("sku",)


class Query(object):
    productcategory = relay.Node.Field(ProductCategoryNode)
    all_productcategory = DjangoFilterConnectionField(ProductCategoryNode)

    productparent = relay.Node.Field(ProductParentNode)
    all_productparents = DjangoFilterConnectionField(ProductParentNode)
    
    productvariant = relay.Node.Field(ProductVariantNode)
    all_productvariants = DjangoFilterConnectionField(ProductVariantNode)

    productimage = relay.Node.Field(ProductImageNode)
    all_productimage = DjangoFilterConnectionField(ProductImageNode)

    productvideo = relay.Node.Field(ProductVideoNode)
    all_productvideo = DjangoFilterConnectionField(ProductVideoNode)

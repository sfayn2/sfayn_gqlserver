
import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField, GlobalIDMultipleChoiceFilter
import django_filters
from django_filters.filters import *
from django.db.models import Sum, F, FloatField
from .models import (
    ProductParent,
    ProductVariant,
    ProductVariantItem,
    ProductVideo,
    ProductImage,
    ProductCategory
)
from django.db.models import Q
from services import get_list_from_global_id

class ProductParentNodeFilter(django_filters.FilterSet):
    keyword = CharFilter(method='or_custom_filter')

    #class Meta:
    #    model = ProductParent
    #    fields = ['keyword']


    def or_custom_filter(self, queryset, name, value):
        value = eval(value) 

        keyword = value.get("keyword")
        minprice = value.get("minprice")
        maxprice = value.get("maxprice")

        brand = value.get("brand") #list of str
        category = value.get("category") #list of str

        queryset  = queryset.filter(Q(title__icontains=keyword)|Q(goods_desc__icontains=keyword))

        if minprice and maxprice:
            queryset = queryset.filter(
                product2variantitem__price__gte=minprice,
                product2variantitem__price__lte=maxprice
            ).distinct()

        if brand:
            queryset = queryset.filter(goods_brand__in=brand.split(","))

        if category:
            final_id = get_list_from_global_id(category)
            queryset = queryset.filter(category_id__in=final_id)


        return queryset


class ProductParentNode(DjangoObjectType):
    class Meta:
        model = ProductParent
        filterset_class = ProductParentNodeFilter
        #filter_fields = {
        #  'parent_sn': ['exact', 'icontains', 'istartswith'],
        #  'title': ['icontains']
        #} 
        interfaces = (relay.Node,)


class ProductCategoryNodeFilter(django_filters.FilterSet):
    id = GlobalIDMultipleChoiceFilter() #filter by List not actually working
    level = django_filters.CharFilter()

class ProductCategoryNode(DjangoObjectType):
    level = graphene.String()
    class Meta:
        model = ProductCategory
        filterset_class = ProductCategoryNodeFilter
        interfaces = (relay.Node,)
        #filter_fields = {
        #  'id': ['in'],
        #  'level': ['exact']
        #} 

    def resolve_level(self, info):
        return self.get_level_display()


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
        filter_fields = ("name",)


class ProductVariantItemNode(DjangoObjectType):
    class Meta:
        model = ProductVariantItem
        interfaces = (relay.Node,)
        #filter_fields = ("sku",)
        filter_fields = {
          'sku': ['exact'],
          'price': ['gte', 'lte']
        } 


class Query(object):
    productcategory = relay.Node.Field(ProductCategoryNode)
    all_productcategory = DjangoFilterConnectionField(ProductCategoryNode)

    productparent = relay.Node.Field(ProductParentNode)
    all_productparents = DjangoFilterConnectionField(ProductParentNode)
    
    #productvariant = relay.Node.Field(ProductVariantNode)
    #all_productvariants = DjangoFilterConnectionField(ProductVariantNode)

    productimage = relay.Node.Field(ProductImageNode)
    all_productimage = DjangoFilterConnectionField(ProductImageNode)

    productvideo = relay.Node.Field(ProductVideoNode)
    all_productvideo = DjangoFilterConnectionField(ProductVideoNode)

    productvariant = relay.Node.Field(ProductVariantNode)
    all_productvariants = DjangoFilterConnectionField(ProductVariantNode)

    productvariantitem = relay.Node.Field(ProductVariantItemNode)
    all_productvariantitems = DjangoFilterConnectionField(ProductVariantItemNode)

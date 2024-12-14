
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
from services import (
    get_list_from_global_id, 
    get_price_min,
    get_price_max,
    get_l3_categories
)


class ProductVariantItemNodeFilter(django_filters.FilterSet):
    sku = django_filters.CharFilter()
    default = django_filters.BooleanFilter()
    #title = django_filters.CharFilter(field_name='parent_sn__title', lookup_expr="icontains")
    keyword = CharFilter(method='or_custom_filter')
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
        )
    )

    def or_custom_filter(self, queryset, name, value):
        value = eval(value) 

        keyword = value.get("keyword")

        brand = value.get("brand") #list of str
        category = value.get("category") #list of str
        level = value.get("level") #list of str


        if keyword:
            #handle main search, filter by brand, category, price
            queryset  = queryset.filter(
                Q(parent_sn__title__icontains=keyword)|
                Q(parent_sn__goods_desc__icontains=keyword)
            )

            if category:
                category_id = get_list_from_global_id(category)
                queryset = queryset.filter(parent_sn__category_id__in=category_id)

        elif category and level:
            #to handle search by parent category
            category_id = get_list_from_global_id(category)
            l3_categories = get_l3_categories(category_id, int(level))
            queryset = queryset.filter(parent_sn__category_id__in=l3_categories)

        if brand:
            queryset = queryset.filter(parent_sn__goods_brand__in=brand)


        return queryset



class ProductVariantItemNode(DjangoObjectType):
    class Meta:
        model = ProductVariantItem
        filterset_class = ProductVariantItemNodeFilter
        interfaces = (relay.Node,)
        #filter_fields = {
        #  'sku': ['exact'],
        #  'price': ['gte', 'lte']
        #} 



class ProductParentNode(DjangoObjectType):
    price_min = graphene.Float()
    price_max = graphene.Float()

    class Meta:
        model = ProductParent
        filter_fields = ("id", )
        interfaces = (relay.Node,)

    def resolve_price_min(self, info):
        return get_price_min(self.id)

    def resolve_price_max(self, info):
        return get_price_max(self.id)

class ProductCategoryNodeFilter(django_filters.FilterSet):
    id = GlobalIDMultipleChoiceFilter() #filter by List not actually working
    level = django_filters.CharFilter()
    parent = django_filters.CharFilter()

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

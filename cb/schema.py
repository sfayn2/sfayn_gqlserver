import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from django.db.models import Sum, F, FloatField
#from django.db.models import F, Sum, FloatField
from services import (
    get_shoppingcart_total_count, 
    get_shoppingcart_group_by_warehouse
)

from .models import (
    Product, 
    ProductWarehouse, 
    ProductOriginalImg, 
    ProductDescImg, 
    ProductParent, 
    ProductCategory, 
    ShoppingCart
)
from .enums import ShopCartMode


class ProductParentFilter(django_filters.FilterSet):
    #having problem so decided to custom filter for __in  
    parent2product__cat__cat_id__in = django_filters.BaseInFilter(
        field_name="parent2product__cat__cat_id", lookup_expr='in'
    )

    class Meta:
        model = ProductParent
        fields = ("parent2product__cat__cat_id",)

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
        filter_fields = ("cat_name", "level", "parent_id", "cat_id")
        interfaces = (relay.Node,)


class ProductNode(DjangoObjectType):
    #having problem so decided to custom filter for __in  
    cat__cat_id__in = django_filters.BaseInFilter(
        field_name="cat__cat_id", 
        lookup_expr='in'
    )
    class Meta:
        model = Product
        interfaces = (relay.Node,)
        filter_fields = {"title": ["exact", "icontains", "istartswith"], 
                         "sku": ["exact"],
                         "cat__cat_name": ["exact", "icontains"],
                         "cat__cat_id": ["exact"]
                         }


class ProductWarehouseNode(DjangoObjectType):
    warehouse_display = graphene.String()
    class Meta:
        model = ProductWarehouse
        filter_fields = ("warehouse",)
        interfaces = (relay.Node,)

    #use to display choice real value
    def resolve_warehouse_display(self, info):
        return self.get_warehouse_display()


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

class ShoppingCartNode(DjangoObjectType):
    class Meta:
        model = ShoppingCart
        exclude_fields = ("user__password",) #dunno why cant hide
        filter_fields = ("product__title", "product__sku", "user__id")
        interfaces = (relay.Node,)

    total_price = graphene.Float()
    total_count = graphene.Float()

    def resolve_total_price(self, info):
        return float(self.product.warehouse.values_list('price', flat=True)[0])*float(self.quantity)

    def resolve_total_count(self, info):
       return get_shoppingcart_total_count(self.user_id) 


class ShoppingCartMutation(graphene.Mutation):
    class Arguments:
        user = graphene.ID(required=True)
        product = graphene.ID(required=True)
        quantity = graphene.ID(required=False)
        mode = graphene.ID(required=True)

    shopping_cart = graphene.Field(ShoppingCartNode)
    ok = graphene.Boolean()

    def mutate(self, info, user, product, mode, quantity=None):

        ok = False

        if ShopCartMode.ADD == int(mode):
            sc = ShoppingCart()
            sc.product_id = product
            sc.user_id = user
            sc.quantity = quantity
            ok = sc.save()

        elif ShopCartMode.UPDATE == int(mode): 
            sc = ShoppingCart.objects.get(product_id=product, user_id=user)
            sc.quantity = quantity
            ok = sc.save()

        elif ShopCartMode.DELETE == int(mode): 
            sc = ShoppingCart.objects.get(product_id=product, user_id=user)
            ok = sc.delete()

        return ShoppingCartMutation(ok=ok, shopping_cart=sc)



from django.contrib.auth import get_user_model
class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class Query1(graphene.AbstractType):
    me = graphene.List(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not logged in!")
        return get_user_model().objects.all()


class WarehouseShoppingCartObjectType(graphene.ObjectType):
    name = graphene.String() #warehouse name
    shopping_cart = DjangoFilterConnectionField(ShoppingCartNode) #i need this to have a filter. but dont need edges nodes here for pagination

class WarehouseShoppingCartListType(graphene.ObjectType):
    warehouses = graphene.List(WarehouseShoppingCartObjectType)
    total_count = graphene.Int()




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

    shopping_cart = relay.Node.Field(ShoppingCartNode)
    all_shopping_cart = DjangoFilterConnectionField(ShoppingCartNode)

    all_shopping_cart_warehouse = graphene.List(WarehouseShoppingCartListType)


    def resolve_all_shopping_cart_warehouse(self, info, **kwargs):
        return get_shoppingcart_group_by_warehouse()


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

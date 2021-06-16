import graphene

from graphene import relay
from graphql_relay import from_global_id
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from django.db.models import Sum, F, FloatField
from .models import (
    ShopCart,
    ShopOrder,
    ShopOrderItem,
)
from .enums import (
    ShopCartMode
)
from product.models import (
    ProductVariant
)


class ShopOrderNode(DjangoObjectType):
    class Meta:
        model = ShopOrder
        filter_fields = ("id",)
        interfaces = (relay.Node,)


class ShopOrderItemNode(DjangoObjectType):
    class Meta:
        model = ShopOrderItem
        filter_fields = ("order_id",)
        interfaces = (relay.Node,)


class ShopCartNode(DjangoObjectType):
    class Meta:
        model = ShopCart
        exclude_fields = ("user__password",) #dunno why cant hide
        filter_fields = ("created_by__id",)
        interfaces = (relay.Node,)

    total_price = graphene.Float()
    total_count = graphene.Float()

    def resolve_total_price(self, info):
        return float(self.product_variant.price)*float(self.quantity)


class ShopCartMutation(graphene.Mutation):
    class Arguments:
        user = graphene.ID(required=True)
        sku = graphene.ID(required=True)
        quantity = graphene.ID(required=False)
        mode = graphene.ID(required=True)

    shopcart = graphene.Field(ShopCartNode)
    ok = graphene.Boolean()

    def mutate(self, info, user, sku, mode, quantity=None):

        ok = False

        #need to convert back the relay id
        #product_variant = from_global_id(product_variant)

        if ShopCartMode.ADD == int(mode):
            pv = ProductVariant.objects.get(sku=sku)
            sc = ShopCart()
            sc.product_variant = pv
            sc.created_by_id = user
            sc.quantity = quantity
            ok = sc.save()

        elif ShopCartMode.UPDATE == int(mode): 
            sc = ShopCart.objects.get(product_variant__sku=sku, created_by_id=user)
            sc.quantity = quantity
            ok = sc.save()

        elif ShopCartMode.DELETE == int(mode): 
            sc = ShopCart.objects.get(product_variant__sku=sku, created_by_id=user)
            ok = sc.delete()

        return ShopCartMutation(ok=ok, shopcart=sc)


class Query(object):
    shopcart = relay.Node.Field(ShopCartNode)
    all_shopcart = DjangoFilterConnectionField(ShopCartNode)

    shoporderitems = relay.Node.Field(ShopOrderItemNode)
    all_shoporderitems = DjangoFilterConnectionField(ShopOrderItemNode)

    shoporder = relay.Node.Field(ShopOrderNode)
    all_shoporder = DjangoFilterConnectionField(ShopOrderNode)

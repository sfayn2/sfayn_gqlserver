import graphene

from graphene import relay
from graphql_relay import from_global_id
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from django.db.models import Sum, F, FloatField
from graphql_jwt.decorators import login_required
from .models import (
    ShopCart,
    ShopOrder,
    ShopOrderItem,
)
from .enums import (
    ShopCartMode
)
from product.models import (
    ProductVariantItem
)


class ShopOrderNode(DjangoObjectType):
    status = graphene.String()
    class Meta:
        model = ShopOrder
        filter_fields = ("id",)
        interfaces = (relay.Node,)

    def resolve_status(self, info):
        for status in self.Status:
            if status.value == int(self.status):
                return status.label

        # below doesnt work for mutation that return non relay result??
        #return self.get_status_display()


class ShopOrderItemNode(DjangoObjectType):
    class Meta:
        model = ShopOrderItem
        filter_fields = ("order_id",)
        interfaces = (relay.Node,)


class ShopCartNode(DjangoObjectType):
    class Meta:
        model = ShopCart
        filter_fields = ("created_by__id",)
        interfaces = (relay.Node,)

    total_price = graphene.Float()
    total_count = graphene.Float()

    def resolve_total_price(self, info):
        return float(self.product_variant.price)*float(self.quantity)


class ShopCartMutation(relay.ClientIDMutation):
    class Input:
        user = graphene.ID(required=True)
        sku = graphene.ID(required=True)
        quantity = graphene.ID(required=False)
        mode = graphene.ID(required=True)

    shopcart = graphene.Field(ShopCartNode)
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, user, sku, mode, quantity=None):

        ok = False
        #need to convert back the relay id
        #product_variant = from_global_id(product_variant)
        user = from_global_id(user)[1] #it returns ('UserNode', '1')

        if ShopCartMode.ADD == int(mode):
            pv = ProductVariantItem.objects.get(sku=sku)
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


class ShopOrderMutation(relay.ClientIDMutation):
    class Input:
        user = graphene.ID(required=True)
        payment = graphene.ID(required=True)
        customer_address = graphene.ID(required=True)
        total_amount = graphene.Float(required=True)

    shoporder = graphene.Field(ShopOrderNode)
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, 
        root, 
        info, 
        user, 
        payment, 
        customer_address,
        total_amount
    ):

        ok = False
        user_id = from_global_id(user)[1] #it returns ('UserNode', '1')
        payment_id = from_global_id(payment)[1]
        customer_address_id = from_global_id(customer_address)[1]

        so = ShopOrder()
        so.payment_method_id = payment_id
        so.customer_address_id = customer_address_id
        so.created_by_id = user_id
        so.total_amount = total_amount
        so.status = so.Status.WAITING_FOR_PAYMENT

        ok = so.save()

        return ShopOrderMutation(ok=ok, shoporder=so)


class ShopOrderItemMutation(relay.ClientIDMutation):
    class Input:
        user = graphene.ID(required=True)
        order = graphene.ID(required=True)
        item = graphene.ID(required=True)

    shoporderitem = graphene.Field(ShopOrderItemNode)
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, 
        root, 
        info, 
        user, 
        order, 
        item,
    ):

        ok = False
        user_id = from_global_id(user)[1] #it returns ('UserNode', '1')
        order_id = from_global_id(order)[1]
        cart_id = from_global_id(item)[1]

        s = ShopOrderItem()
        s.order_id = order_id
        s.shopcart_id = cart_id
        s.created_by_id = user_id

        ok = s.save()

        return ShopOrderItemMutation(ok=ok, shoporderitem=s)


class ShopOrderStatusMutation(relay.ClientIDMutation):
    class Input:
        order = graphene.ID(required=True)
        status = graphene.ID(required=True)

    shoporder = graphene.Field(ShopOrderNode)
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, 
        root, 
        info, 
        order, 
        status
    ):

        ok = False
        order_id = from_global_id(order)[1] 

        so = ShopOrder.objects.get(id=order_id)
        so.status = status

        ok = so.save()

        return ShopOrderStatusMutation(ok=ok, shoporder=so)


class Query(object):
    shopcart = relay.Node.Field(ShopCartNode)
    all_shopcart = DjangoFilterConnectionField(ShopCartNode)

    shoporderitems = relay.Node.Field(ShopOrderItemNode)
    all_shoporderitems = DjangoFilterConnectionField(ShopOrderItemNode)

    shoporder = relay.Node.Field(ShopOrderNode)
    all_shoporder = DjangoFilterConnectionField(ShopOrderNode)

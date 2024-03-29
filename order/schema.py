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
    Order,
    OrderItem,
)
from product.models import (
    ProductVariantItem
)


class OrderNode(DjangoObjectType):
    status = graphene.String()
    class Meta:
        model = Order
        filter_fields = ("id",)
        interfaces = (relay.Node,)

    def resolve_status(self, info):
        for status in self.Status:
            if status.value == int(self.status):
                return status.label

        # below doesnt work for mutation that return non relay result??
        #return self.get_status_display()


class OrderItemNode(DjangoObjectType):
    class Meta:
        model = OrderItem
        filter_fields = ("order_id",)
        interfaces = (relay.Node,)


class OrderMutation(relay.ClientIDMutation):
    class Input:
        user = graphene.ID(required=True)
        payment = graphene.ID(required=True)
        shipping_address = graphene.ID(required=True)
        tax = graphene.ID(required=True)
        shipping_fee = graphene.Float(required=False) #optional?
        discount_fee = graphene.Float(required=False) #optional?
        tax_rate = graphene.Float(required=False) #optional?
        total_amount = graphene.Float(required=True)
        notes = graphene.String(required=False)

    order = graphene.Field(OrderNode)
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, 
        root, 
        info, 
        user, 
        payment, 
        shipping_address,
        tax,
        total_amount,
        shipping_fee,
        discount_fee,
        tax_rate,
        notes
    ):

        ok = False
        user_id = from_global_id(user)[1] #it returns ('UserNode', '1')
        payment_id = from_global_id(payment)[1]
        shipping_address_id = from_global_id(shipping_address)[1]
        tax_id = from_global_id(tax)[1]

        so = Order()
        so.payment_method_id = payment_id
        so.shipping_address_id = shipping_address_id
        so.tax_id = tax_id
        so.created_by_id = user_id
        so.shipping_fee = shipping_fee
        so.discount_fee = discount_fee
        so.tax_rate = tax_rate
        so.total_amount = total_amount
        so.notes = notes
        so.status = so.Status.WAITING_FOR_PAYMENT

        ok = so.save()

        return OrderMutation(ok=ok, order=so)


class OrderItemMutation(relay.ClientIDMutation):
    class Input:
        user = graphene.ID(required=True)
        order = graphene.ID(required=True)
        item = graphene.ID(required=True)

    orderitem = graphene.Field(OrderItemNode)
    ok = graphene.Boolean()

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls, 
        root, 
        info, 
        user, 
        order, 
        product,
        quantity
    ):

        ok = False
        user_id = from_global_id(user)[1] #it returns ('UserNode', '1')
        order_id = from_global_id(order)[1]
        #cart_id = from_global_id(item)[1] > let front end store do this?
        product_variant_id =  from_global_id(product)[1]
        ordered_quantity = quantity

        s = OrderItem()
        s.order_id = order_id
        s.created_by_id = user_id
        s.product_variant_id = product_variant_id

        product_variant = ProductVariantItem.objects.get(id=product_variant_id)
        if product_variant.quantity < ordered_quantity:
            raise "Not enough stock!"

        s.quantity = quantity
        s.locked_in_price = product_variant.price

        ok = s.save()

        return OrderItemMutation(ok=ok, orderitem=s)


class OrderStatusMutation(relay.ClientIDMutation):
    class Input:
        order = graphene.ID(required=True)
        status = graphene.ID(required=True)

    order = graphene.Field(OrderNode)
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

        so = Order.objects.get(id=order_id)
        so.status = status

        ok = so.save()

        return OrderStatusMutation(ok=ok, order=so)


class Query(object):

    orderitems = relay.Node.Field(OrderItemNode)
    all_orderitems = DjangoFilterConnectionField(OrderItemNode)

    order = relay.Node.Field(OrderNode)
    all_order = DjangoFilterConnectionField(OrderNode)


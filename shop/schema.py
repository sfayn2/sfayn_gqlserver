import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from django.db.models import Sum, F, FloatField
from .models import (
    ShopCart
)


class ShopCartNode(DjangoObjectType):
    class Meta:
        model = ShopCart
        exclude_fields = ("user__password",) #dunno why cant hide
        filter_fields = ("created_by__id",)
        interfaces = (relay.Node,)

    total_price = graphene.Float()
    total_count = graphene.Float()


class Query(object):
    shopcart = relay.Node.Field(ShopCartNode)
    all_shopcart = DjangoFilterConnectionField(ShopCartNode)


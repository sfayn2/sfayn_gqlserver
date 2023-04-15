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
    Discount,
)


class DiscountNode(DjangoObjectType):
    class Meta:
        model = Discount
        filter_fields = ("id",)
        interfaces = (relay.Node,)


class Query(object):

    discount = relay.Node.Field(DiscountNode)
    all_discount = DjangoFilterConnectionField(DiscountNode)


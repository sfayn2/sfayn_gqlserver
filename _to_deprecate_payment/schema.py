import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from .models import (
    PaymentMethod
)


class PaymentMethodNode(DjangoObjectType):
    class Meta:
        model = PaymentMethod
        filter_fields = ("created_by_id",)
        interfaces = (relay.Node,)


class Query(object):
    payment_method = relay.Node.Field(PaymentMethodNode)
    all_payment_method = DjangoFilterConnectionField(PaymentMethodNode)

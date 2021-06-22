
import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from .models import (
    CustomerAddress
)

class CustomerAddressNode(DjangoObjectType):
    class Meta:
        model = CustomerAddress
        filter_fields = ("created_by_id",)
        interfaces = (relay.Node,)


class Query(object):
    customeraddress = relay.Node.Field(CustomerAddressNode)
    all_customeraddress = DjangoFilterConnectionField(CustomerAddressNode)

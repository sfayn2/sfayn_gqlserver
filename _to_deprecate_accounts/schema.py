
import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from django.contrib.auth.models import (
    User
)

from .models import Address

class AddressNode(DjangoObjectType):
    class Meta:
        model = Address
        filter_fields = ("created_by_id",)
        interfaces = (relay.Node,)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ("id",)
        interfaces = (relay.Node,)
        exclude = ("password",)


class Query(object):
    user = relay.Node.Field(UserNode)
    all_user = DjangoFilterConnectionField(UserNode)

    address = relay.Node.Field(AddressNode)
    all_address = DjangoFilterConnectionField(AddressNode)

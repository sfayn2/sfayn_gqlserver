
import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from django.contrib.auth.models import (
    User
)

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ("id",)
        interfaces = (relay.Node,)
        exclude = ("password",)


class Query(object):
    user = relay.Node.Field(UserNode)
    all_user = DjangoFilterConnectionField(UserNode)


import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField, GlobalIDMultipleChoiceFilter
import django_filters
from django_filters.filters import *
from django.db.models import Sum, F, FloatField
from .models import (
    Tag,
    TagItem,
)

class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = ("id", )
        interfaces = (relay.Node,)


class TagItemNode(DjangoObjectType):
    class Meta:
        model = TagItem
        filter_fields = ("id", )
        interfaces = (relay.Node,)




class Query(object):
    tag = relay.Node.Field(TagNode)
    all_tag = DjangoFilterConnectionField(TagNode)

    tagitem = relay.Node.Field(TagItemNode)
    all_tagitem = DjangoFilterConnectionField(TagItemNode)



import graphene

from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from django_filters.filters import *
from django.db.models import Sum, F, FloatField
from .models import (
    PromotionalBanner
)


class PromotionalBannerNode(DjangoObjectType):
    class Meta:
        model = PromotionalBanner
        interfaces = (relay.Node,)
        filter_fields = ("created_by", )


class Query(object):
    promotionalbanner = relay.Node.Field(PromotionalBannerNode)
    all_promotionalbanner = DjangoFilterConnectionField(PromotionalBannerNode)

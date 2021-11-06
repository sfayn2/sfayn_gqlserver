
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


class PromotionalBannerNodeFilter(django_filters.FilterSet):

	# need to define fields of valid choices in orderBy
    order_by = django_filters.OrderingFilter(
        fields=(
            ('display_order', 'display_order'),
        )
    )

    class Meta:
        model = PromotionalBanner
        fields = ('created_by', 'order_by')



class PromotionalBannerNode(DjangoObjectType):
    class Meta:
        model = PromotionalBanner
        interfaces = (relay.Node,)
        filterset_class = PromotionalBannerNodeFilter


class Query(object):
    promotionalbanner = relay.Node.Field(PromotionalBannerNode)
    all_promotionalbanner = DjangoFilterConnectionField(PromotionalBannerNode)

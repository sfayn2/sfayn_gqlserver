import graphene
from graphene import relay
from ddd.order_management.infrastructure import adapters
from ddd.order_management.application import (
    message_bus, queries
  )
from ddd.order_management.presentation.graphql import object_types, input_types

class ShippingOptionsQuery(graphene.ObjectType):

    #shipping_options = graphene.List(ShippingDetailsType)
    shipping_options_by_order_id = graphene.List(input_types.ShippingDetailsType, order_id=graphene.String(required=True))
    def resolve_shipping_options_by_order_id(root, info, order_id):
        query = queries.ShippingOptionsQuery(order_id=order_id)
        shipping_options = message_bus.handle(query, adapters.unit_of_work.DjangoOrderUnitOfWork())

        return shipping_options
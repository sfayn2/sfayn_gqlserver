import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, queries
  )
from ddd.order_management.presentation.graphql import object_types, input_types

class ListShippingOptionsQuery(graphene.ObjectType):

    #shipping_options = graphene.List(ShippingDetailsType)
    list_shipping_options_by_order_id = graphene.List(object_types.ShippingDetailsType, order_id=graphene.String(required=True))
    def resolve_list_shipping_options_by_order_id(root, info, order_id):
        token = common.get_token_from_context(info)
        query = queries.ListShippingOptionsQuery(order_id=order_id, token=token)
        shipping_options = message_bus.handle(query)

        return shipping_options
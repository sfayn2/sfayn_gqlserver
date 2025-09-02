import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, queries
  )
from ddd.order_management.presentation.graphql import object_types, input_types
from ddd.order_management.infrastructure import (
    access_control1,
)

class ListShippingOptionsQuery(graphene.ObjectType):

    #shipping_options = graphene.List(ShippingDetailsType)
    list_shipping_options_by_order_id = graphene.List(object_types.ShippingDetailsType, order_id=graphene.String(required=True))
    def resolve_list_shipping_options_by_order_id(root, info, order_id):
        token = common.get_token_from_context(info)
        user_ctx = access_control1.get_user_context(token)
        query = queries.ListShippingOptionsQuery(order_id=order_id)
        shipping_options = message_bus.handle(query, user_ctx=user_ctx)

        return shipping_options
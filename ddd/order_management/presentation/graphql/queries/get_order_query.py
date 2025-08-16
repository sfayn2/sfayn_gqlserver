import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, queries
  )
from ddd.order_management.presentation.graphql import object_types, input_types, common

class GetOrderQuery(graphene.ObjectType):

    get_order_by_order_id = graphene.Field(object_types.OrderType, order_id=graphene.String(required=True))
    def resolve_get_order_by_order_id(root, info, order_id):
        token = common.get_token_from_context(info)
        query = queries.GetOrderQuery(order_id=order_id, token=token)
        order = message_bus.handle(query)

        return order
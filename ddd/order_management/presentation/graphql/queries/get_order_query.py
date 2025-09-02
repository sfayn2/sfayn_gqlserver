import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, queries
  )
from ddd.order_management.presentation.graphql import object_types, input_types, common
from ddd.order_management.infrastructure import (
    access_control1,
)

class GetOrderQuery(graphene.ObjectType):

    get_order_by_order_id = graphene.Field(object_types.OrderType, order_id=graphene.String(required=True))
    def resolve_get_order_by_order_id(root, info, order_id):
        token = common.get_token_from_context(info)
        user_ctx = access_control1.get_user_context(token)
        query = queries.GetOrderQuery(order_id=order_id)
        order = message_bus.handle(query, user_ctx=user_ctx)

        return order
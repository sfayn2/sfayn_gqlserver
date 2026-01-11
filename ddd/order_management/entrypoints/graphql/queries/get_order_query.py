import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, queries, dtos
  )
from ddd.order_management.entrypoints.graphql import object_types, input_types, common

class GetOrderQuery(graphene.ObjectType):

    get_order_by_order_id = graphene.Field(object_types.OrderType, order_id=graphene.String(required=True))
    def resolve_get_order_by_order_id(root, info, order_id):
        token = common.get_token_from_context(info)
        request_tenant_id = common.get_tenant_id(token)
        #user_ctx = access_control1.get_user_context(token)

        # 1. Create a DTO with the raw necessary context data
        context_data = dtos.RequestContextDTO( # A new DTO we define
            token=token,
            tenant_id=request_tenant_id
        )

        query = queries.GetOrderQuery(order_id=order_id)

        # 2. Pass this raw context data DTO to the message bus handler
        # The message bus (Application Layer) should handle resolving authentication/authorization logic.
        order = message_bus.handle(query, context_data=context_data)

        return order
import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, queries, dtos
  )
from ddd.order_management.entrypoints.graphql import object_types, input_types, common

class GetOrderQuery(graphene.ObjectType):

    get_order_by_order_id = graphene.Field(object_types.OrderType, tenant_id=graphene.String(required=True), order_id=graphene.String(required=True))
    def resolve_get_order_by_order_id(root, info, tenant_id, order_id):
        context_data = common.get_request_context(info, **{"tenant_id": tenant_id})

        query = queries.GetOrderQuery(order_id=order_id)

        # 2. Pass this raw context data DTO to the message bus handler
        # The message bus (Application Layer) should handle resolving authentication/authorization logic.
        order = message_bus.handle(query, context_data=context_data)

        return order
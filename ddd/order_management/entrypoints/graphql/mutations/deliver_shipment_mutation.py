import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands, dtos
  )
from ddd.order_management.entrypoints.graphql import object_types, common, input_types


# ==========================
# Mutations 
# ===================
class DeliverShipmentMutation(relay.ClientIDMutation):
    class Input:
        tenant_id = graphene.String(required=True)
        order_id = graphene.String(required=True)
        shipment_id = graphene.String(required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        context_data = common.get_request_context(info, **input)

        command = commands.DeliverShipmentCommand.model_validate(input)

        # 2. Pass this raw context data DTO to the message bus handler
        # The message bus (Application Layer) should handle resolving authentication/authorization logic.
        result = message_bus.handle(command, context_data=context_data)

        return cls(result=object_types.ResponseType(**result.model_dump()))


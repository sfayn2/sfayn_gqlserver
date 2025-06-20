import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.graphql import object_types


# ==========================
# Mutations 
# ===================
class MarkAsShippedMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        command = commands.ShipOrderCommand.model_validate(input)
        result = message_bus.handle(command)

        return cls(result=object_types.ResponseType(**result.model_dump()))


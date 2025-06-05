import graphene
from graphene import relay
from ddd.order_management.infrastructure import adapters
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.graphql import object_types


# ==========================
# Mutations 
# ===================
class AddShippingTrackingReferenceMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String()
        shipping_reference = graphene.String()

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        command = commands.AddShippingTrackingReferenceCommand.model_validate(input)
        result = message_bus.handle(command, adapters.unit_of_work.DjangoOrderUnitOfWork())

        return cls(result=object_types.ResponseType(**result.model_dump()))


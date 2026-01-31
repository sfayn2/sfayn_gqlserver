import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands, dtos
  )
from ddd.order_management.entrypoints.graphql import object_types, common, input_types


# ==========================
# Mutations 
# ===================
class AddOrderMutation(relay.ClientIDMutation):
    class Input:
        tenant_id = graphene.String(required=True)
        external_ref = graphene.String(required=True)
        customer_details = graphene.Field(input_types.CustomerDetailsInput, required=True)
        product_skus = graphene.List(input_types.ProductSkusInput, required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        context_data = common.get_request_context(info, **input)

        command = commands.AddOrderCommand.model_validate(input)

        # 2. Pass this raw context data DTO to the message bus handler
        # The message bus (Application Layer) should handle resolving authentication/authorization logic.
        result = message_bus.handle(command, context_data=context_data)

        return cls(result=object_types.ResponseType(**result.model_dump()))


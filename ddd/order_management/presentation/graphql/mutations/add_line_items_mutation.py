import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.graphql import object_types, input_types, common

class AddLineItemsMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True)
        product_skus = graphene.List(input_types.ProductSkusInput, required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        input["token"] = common.get_token_from_context(info)
        command = commands.AddLineItemsCommand.model_validate(input)
        result = message_bus.handle(command)
        return cls(result=object_types.ResponseType(**result.model_dump()))
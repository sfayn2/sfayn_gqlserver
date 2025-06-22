import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.graphql import object_types, input_types

class CheckoutItemsMutation(relay.ClientIDMutation):
    class Input:
        vendor_id = graphene.String(required=True)
        customer_id = graphene.String(required=True)
        address = graphene.Field(input_types.AddressInput, required=True)
        product_skus = graphene.List(input_types.ProductSkusInput, required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        command = commands.CheckoutItemsCommand.model_validate(input)
        result = message_bus.handle(command)
        return cls(result=object_types.ResponseType(**result.model_dump()))
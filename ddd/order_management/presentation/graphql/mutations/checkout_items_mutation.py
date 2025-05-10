import graphene
from graphene import relay
from ddd.order_management.infrastructure import adapters
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.graphql import object_types, input_types

class CheckoutItemsMutation(relay.ClientIDMutation):
    class Input:
        customer_details = graphene.Field(input_types.CustomerDetailsInput, required=True)
        shipping_address = graphene.Field(input_types.AddressInput, required=True)
        line_items = graphene.List(input_types.LineItemInput, required=True)

    order = graphene.Field(object_types.OrderResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        command = commands.CheckoutItemsCommand.model_validate(input)
        draft_order = message_bus.handle(command, adapters.unit_of_work.DjangoOrderUnitOfWork())
        return cls(order=object_types.OrderResponseType(**draft_order.model_dump()))
import graphene
from graphene import relay
from ddd.order_management.infrastructure import adapters
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.graphql import object_types, input_types

class SelectShippingOptionMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True)
        shipping_details = graphene.Field(input_types.ShippingDetailsInput, required=True)


    #TODO: should return Shipping details response
    order = graphene.Field(object_types.OrderResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        command = commands.SelectShippingOptionCommand.model_validate(input)
        shipping_option = message_bus.handle(command, adapters.unit_of_work.DjangoOrderUnitOfWork())
        return cls(order=object_types.OrderResponseType(**shipping_option.model_dump()))
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
class PlaceOrderMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String()

    order = graphene.Field(object_types.OrderResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        command = commands.PlaceOrderCommand.model_validate(input)
        placed_order = message_bus.handle(command, adapters.unit_of_work.DjangoOrderUnitOfWork())
        #placed order status only in Pending; once payment is confirmed ; webhook will trigger and call api to confirm order

        return cls(order=object_types.OrderResponseType(**placed_order.model_dump()))


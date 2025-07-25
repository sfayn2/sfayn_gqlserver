import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands
  )
from ddd.order_management.presentation.graphql import object_types, common


# ==========================
# Mutations 
# ===================
class PlaceOrderMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        input["token"] = common.get_token_from_context(info)
        command = commands.PlaceOrderCommand.model_validate(input)
        result = message_bus.handle(command)
        #placed order status only in Pending; once payment is confirmed ; webhook will trigger and call api to confirm order

        return cls(result=object_types.ResponseType(**result.model_dump()))


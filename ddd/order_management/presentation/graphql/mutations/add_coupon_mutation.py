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
        coupon_code = graphene.String()

    order = graphene.Field(object_types.OrderResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        command = commands.AddCouponCommand.model_validate(input)
        order_w_coupon = message_bus.handle(command, adapters.unit_of_work.DjangoOrderUnitOfWork())

        return cls(order=object_types.OrderResponseType(**order_w_coupon.model_dump()))


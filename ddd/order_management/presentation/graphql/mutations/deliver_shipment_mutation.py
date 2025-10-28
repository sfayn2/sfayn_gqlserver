import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands, access_control_service
  )
from ddd.order_management.presentation.graphql import object_types, common, input_types


# ==========================
# Mutations 
# ===================
class DeliverShipmentMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True)
        shipment_id = graphene.String(required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        token = common.get_token_from_context(info)
        request_tenant_id = common.get_tenant_id(token)

        access_control = access_control_service.AccessControlService.resolve(request_tenant_id)
        user_ctx = access_control.get_user_context(token, request_tenant_id)


        command = commands.DeliverShipmentCommand.model_validate(input)

        result = message_bus.handle(command, access_control=access_control, user_ctx=user_ctx)

        return cls(result=object_types.ResponseType(**result.model_dump()))


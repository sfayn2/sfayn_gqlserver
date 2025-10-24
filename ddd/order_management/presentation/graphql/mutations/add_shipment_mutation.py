import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands, access_control_service
  )
from ddd.order_management.presentation.graphql import object_types, common, input_types


# ==========================
# Mutations 
# ===================
class AddShipmentMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True)
        shipment_address = graphene.Field(input_types.AddressInput, required=True)
        shipment_items = graphene.List(input_types.ShipmentItemInput, required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        token = common.get_token_from_context(info)
        tenant_id = common.get_tenant_id(token)

        access_control = access_control_service.AccessControlService.resolve(tenant_id)
        user_ctx = access_control.get_user_context(token)

        # verify tenant_id
        if user_ctx.tenant_id != tenant_id:
            raise exceptions.AccessControlException(f"Tenant mismatch token={user_ctx.tenant_id}, request={command.tenant_id}")

        command = commands.AddShipmentCommand.model_validate(input)

        result = message_bus.handle(command, access_control=access_control, user_ctx=user_ctx)

        return cls(result=object_types.ResponseType(**result.model_dump()))


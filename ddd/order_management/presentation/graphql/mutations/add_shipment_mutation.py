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
        shipment_mode = graphene.String(required=True) # pickup, dropoff, warehouse
        shipment_provider = graphene.String(required=True)

        # package
        package_weight_kg = graphene.Decimal(required=False)
        package_length_cm = graphene.Decimal(required=False)
        package_width_cm = graphene.Decimal(required=False)
        package_height_cm = graphene.Decimal(required=False)

        # pickup mode
        pickup_address = graphene.Field(input_types.AddressInput, required=False)
        pickup_window_start = graphene.DateTime(required=False)
        pickup_window_end = graphene.DateTime(required=False)
        pickup_instructions = graphene.String(required=False)

        # destination / items
        shipment_address = graphene.Field(input_types.AddressInput, required=True)
        shipment_items = graphene.List(input_types.ShipmentItemInput, required=True)

        instructions = graphene.String(required=True)

    result = graphene.Field(object_types.ResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        token = common.get_token_from_context(info)
        request_tenant_id = common.get_tenant_id(token)

        access_control = access_control_service.AccessControlService.resolve(request_tenant_id)
        user_ctx = access_control.get_user_context(token, request_tenant_id)


        command = commands.AddShipmentCommand.model_validate(input)

        result = message_bus.handle(command, access_control=access_control, user_ctx=user_ctx)

        return cls(result=object_types.ResponseType(**result.model_dump()))


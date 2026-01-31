import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands, dtos
  )
from ddd.order_management.entrypoints.graphql import object_types, common, input_types


# ==========================
# Mutations 
# ===================
class AddShipmentMutation(relay.ClientIDMutation):
    class Input:
        tenant_id = graphene.String(required=True)
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
        context_data = common.get_request_context(info, **input)

        command = commands.AddShipmentCommand.model_validate(input)

        # 2. Pass this raw context data DTO to the message bus handler
        # The message bus (Application Layer) should handle resolving authentication/authorization logic.
        result = message_bus.handle(command, context_data=context_data)

        return cls(result=object_types.ResponseType(**result.model_dump()))


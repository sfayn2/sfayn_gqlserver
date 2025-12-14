import graphene
from graphene.types.generic import GenericScalar
from ddd.order_management.application import (
    message_bus, queries, dtos, enums
  )

# Graphql enums type
GrapheneOrderStatus = graphene.Enum.from_enum(enums.OrderStatus)
GrapheneShipmentMethod = graphene.Enum.from_enum(enums.ShipmentMethod)
GrapheneShipmentStatus = graphene.Enum.from_enum(enums.ShipmentStatus)

# ====================
# Object Types
# ====================
class MoneyType(graphene.ObjectType):
    amount = graphene.Decimal(required=True)
    currency = graphene.String(required=True)

class AddressType(graphene.ObjectType):
    line1 = graphene.String(required=True)
    city = graphene.String(required=True)
    country = graphene.String(required=True)
    line2 = graphene.String(required=False)
    state = graphene.String(required=False)

    #The best practice for postal codes is to treat them as strings, not integers, because they carry formatting, leading zeros, or letters that numerical types cannot handle.
    postal = graphene.String(required=False)

class PackageType(graphene.ObjectType):
    weight = graphene.Decimal()
    #dimensions = graphene.List(graphene.Int)

class CustomerDetailsType(graphene.ObjectType):
    customer_id = graphene.String(required=False)
    name = graphene.String()
    email = graphene.String()

class LineItemType(graphene.ObjectType):
    product_sku = graphene.String()
    product_name = graphene.String()
    order_quantity = graphene.Int()
    vendor_id = graphene.String()
    product_price = graphene.Field(MoneyType)
    package = graphene.Field(PackageType)

class ShipmentItemType(graphene.ObjectType):
    line_item = graphene.Field(LineItemType)
    quantity = graphene.Int()
    shipment_item_id = graphene.String(required=False)

class ShipmentType(graphene.ObjectType):
    shipment_id = graphene.String()

    shipment_address = graphene.Field(AddressType)
    shipment_provider = graphene.String(required=False)
    shipment_mode = graphene.Field(GrapheneShipmentMethod, required=False) # pickup, dropoff, warehouse

    # package
    package_weight_kg = graphene.Decimal(required=False)
    package_length_cm = graphene.Decimal(required=False)
    package_width_cm = graphene.Decimal(required=False)
    package_height_cm = graphene.Decimal(required=False)

    # pickup mode
    pickup_address = graphene.Field(AddressType, required=False)
    pickup_window_start = graphene.DateTime(required=False)
    pickup_window_end = graphene.DateTime(required=False)
    pickup_instructions = graphene.String(required=False)


    tracking_reference = graphene.String(required=False)
    label_url = graphene.String(required=False)


    shipment_amount = graphene.Field(MoneyType)
    shipment_status = GrapheneShipmentStatus()
    shipment_items = graphene.Field(ShipmentItemType)

class OrderType(graphene.ObjectType):
    order_id = graphene.String()
    line_items = graphene.List(LineItemType)
    shipments = graphene.List(ShipmentType)
    customer_details = graphene.Field(CustomerDetailsType)
    currency = graphene.String()
    tenant_id = graphene.String()
    order_status = GrapheneOrderStatus()
    date_modified = graphene.DateTime()
    date_created = graphene.String()

class ResponseType(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
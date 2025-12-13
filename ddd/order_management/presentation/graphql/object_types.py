import graphene
from graphene.types.generic import GenericScalar
from ddd.order_management.application import (
    message_bus, queries, dtos, enums
  )
#from ddd.order_management.domain import enums

GrapheneOrderStatus = graphene.Enum.from_enum(enums.OrderStatus)

# ====================
# Object Types
# ====================
class MoneyType(graphene.ObjectType):
    amount = graphene.Decimal(required=True)
    currency = graphene.String(required=True)

class AddressType(graphene.ObjectType):
    line1 = graphene.String(required=True)
    city = graphene.String(required=True)
    state = graphene.String(required=True)
    line2 = graphene.String(required=False)
    state = graphene.String(required=False)
    postal = graphene.Int(required=False)

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
    #pickup_address: graphene.Field(AddressType)
    product_price = graphene.Field(MoneyType)
    package = graphene.Field(PackageType)


class OrderType(graphene.ObjectType):
    order_id = graphene.String()
    line_items = graphene.List(LineItemType)
    customer_details = graphene.Field(CustomerDetailsType)
    currency = graphene.String()
    tenant_id = graphene.String()
    order_status = GrapheneOrderStatus()
    date_modified = graphene.DateTime()
    date_created = graphene.String()

class ResponseType(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
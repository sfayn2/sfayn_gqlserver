import graphene
from graphene.types.generic import GenericScalar

# ====================
# Input Types
# ====================
class MoneyInput(graphene.InputObjectType):
    amount = graphene.Decimal(required=True)
    currency = graphene.String(required=True)

class AddressInput(graphene.InputObjectType):
    line1 = graphene.String(required=True)
    city = graphene.String(required=True)
    country = graphene.String(required=True)
    line2 = graphene.String(required=False)
    state = graphene.String(required=False)
    postal = graphene.Int(required=False)

class ShipmentItemInput(graphene.InputObjectType):
    product_sku = graphene.String(required=True)
    quantity = graphene.Int(required=True)
    vendor_id = graphene.String(required=True)

class CustomerDetailsInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)

class ProductSkusInput(graphene.InputObjectType):
    product_sku = graphene.String(required=True)
    order_quantity = graphene.Int(required=True)
    vendor_id = graphene.String(required=True)
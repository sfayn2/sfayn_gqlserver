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
    customer_id = graphene.String(required=False)
    name = graphene.String(required=True)
    email = graphene.String(required=True)

class PackageInput(graphene.InputObjectType):
    weight_kg = graphene.Decimal()

class ProductSkusInput(graphene.InputObjectType):
    product_sku = graphene.String(required=True)
    product_name = graphene.String(required=True)
    product_price = graphene.Field(MoneyInput, required=True)
    order_quantity = graphene.Int(required=True)
    vendor_id = graphene.String(required=True)
    package = graphene.Field(PackageInput, required=False)
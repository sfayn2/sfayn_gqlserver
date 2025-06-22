import graphene
from graphene.types.generic import GenericScalar

# ====================
# Input Types
# ====================
class MoneyInput(graphene.InputObjectType):
    amount = graphene.Decimal(required=True)
    currency = graphene.String(required=True)

class VendorDetailsInput(graphene.InputObjectType):
    vendor_id = graphene.String(required=True)
    #name = graphene.String(required=True) #dummy only? it will still get from db
    #country = graphene.String(required=True) #dummy only it wil still get from db

class PackageInput(graphene.InputObjectType):
    weight = graphene.Decimal(required=True)
    dimensions = graphene.List(graphene.Int, required=True)

#class LineItemInput(graphene.InputObjectType):
#    product_sku = graphene.String(required=True)
#    product_name = graphene.String(required=True)
#    vendor = graphene.Field(VendorDetailsInput, required=True)
#    product_category = graphene.String(required=True)
#    order_quantity = graphene.Int(required=True)
#    options = GenericScalar(required=True)
#    product_price = graphene.Field(MoneyInput, required=True)
#    package = graphene.Field(PackageInput, required=True)
#
class AddressInput(graphene.InputObjectType):
    street = graphene.String(required=True)
    city = graphene.String(required=True)
    state = graphene.String(required=True)
    postal = graphene.String(required=True)
    country = graphene.String(required=True)
#
#class CustomerDetailsInput(graphene.InputObjectType):
#    first_name = graphene.String(required=True)
#    last_name = graphene.String(required=True)
#    email = graphene.String(required=True)

class ShippingDetailsInput(graphene.InputObjectType):
    method = graphene.String(required=True)
    delivery_time = graphene.String(required=True)
    cost = graphene.Field(MoneyInput, required=True)

class PaymentDetailsInput(graphene.InputObjectType):
    method = graphene.String(required=True)
    paid_amount = graphene.Field(MoneyInput, required=True)
    transaction_id = graphene.String(required=True)


class CouponInput(graphene.InputObjectType):
    coupon_code = graphene.String(required=True)

class ProductSkusInput(graphene.InputObjectType):
    product_sku = graphene.String(required=True)
    order_quantity = graphene.Int(required=True)
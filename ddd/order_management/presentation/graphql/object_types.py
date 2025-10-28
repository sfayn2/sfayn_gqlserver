import graphene
from graphene.types.generic import GenericScalar

# ====================
# Object Types
# ====================
class MoneyType(graphene.ObjectType):
    amount = graphene.Decimal(required=True)
    currency = graphene.String(required=True)

class ShippingDetailsType(graphene.ObjectType):
    method = graphene.String(required=True)
    delivery_time = graphene.String(required=True)
    cost = graphene.Field(MoneyType, required=True)

class AddressType(graphene.ObjectType):
    street = graphene.String(required=True)
    city = graphene.String(required=True)
    state = graphene.String(required=True)
    postal = graphene.String(required=True)
    country = graphene.String(required=True)

class PaymentDetailsType(graphene.ObjectType):
    method = graphene.String(required=True)
    paid_amount = graphene.Field(MoneyType, required=True)
    transaction_id = graphene.String(required=True)

class OrderResponseType(graphene.ObjectType):
    order_id = graphene.String()
    order_status = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()
    tax_details = graphene.List(graphene.String)
    offer_details = graphene.List(graphene.String)
    shipping_details = graphene.Field(ShippingDetailsType)
    payment_details = graphene.Field(PaymentDetailsType)
    tax_amount  = graphene.Field(MoneyType)
    total_discounts_fee = graphene.Field(MoneyType)
    final_amount = graphene.Field(MoneyType)

class VendorDetailsType(graphene.ObjectType):
    vendor_id = graphene.String()
    name = graphene.String() 
    country = graphene.String() 

class PackageType(graphene.ObjectType):
    weight = graphene.Decimal()
    dimensions = graphene.List(graphene.Int)

class CustomerDetailsType(graphene.ObjectType):
    customer_id = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()

class CouponType(graphene.ObjectType):
    coupon_code = graphene.String()
    start_date = graphene.DateTime()
    end_date = graphene.DateTime()
    is_active = graphene.Boolean()

class LineItemType(graphene.ObjectType):
    product_sku = graphene.String()
    product_name = graphene.String()
    vendor = graphene.Field(VendorDetailsType)
    product_category = graphene.String()
    order_quantity = graphene.Int()
    options = GenericScalar()
    product_price = graphene.Field(MoneyType)
    package = graphene.Field(PackageType)

class OrderType(graphene.ObjectType):
    order_id = graphene.String()
    date_created = graphene.String()
    destination = graphene.Field(AddressType)
    line_items = graphene.List(LineItemType)
    customer_details = graphene.Field(CustomerDetailsType)
    shipping_details = graphene.Field(ShippingDetailsType)
    payment_details = graphene.Field(PaymentDetailsType)
    cancellation_reason = graphene.String()
    total_discounts_fee = graphene.Field(MoneyType)
    offer_detail = graphene.List(graphene.String)
    tax_details = graphene.List(graphene.String)
    tax_amount = graphene.Field(MoneyType)
    total_amount = graphene.Field(MoneyType)
    final_amount = graphene.Field(MoneyType)
    tracking_reference = graphene.String()
    coupons = graphene.List(CouponType)
    order_status = graphene.String()
    currency = graphene.String()
    date_modified = graphene.DateTime()

class ResponseType(graphene.ObjectType):
    success = graphene.Boolean()
    message = graphene.String()
import graphene

# ====================
# Object Types
# ====================
class MoneyType(graphene.ObjectType):
    amount = graphene.Float(required=True)
    currency = graphene.String(required=True)

class ShippingDetailsType(graphene.ObjectType):
    method = graphene.String(required=True)
    delivery_time = graphene.String(required=True)
    cost = graphene.Field(MoneyType, required=True)

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

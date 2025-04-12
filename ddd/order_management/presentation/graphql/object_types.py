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

class OrderType(graphene.ObjectType):
    order_id: graphene.String()
    date_created: datetime 
    destination: AddressDTO
    line_items: List[LineItemDTO]
    customer_details: Optional[CustomerDetailsDTO]
    shipping_details: Optional[ShippingDetailsDTO]
    payment_details: Optional[PaymentDetailsDTO]
    cancellation_reason: Optional[str]
    total_discounts_fee: Optional[MoneyDTO]
    offer_details: Optional[List[str]]
    tax_details: Optional[List[str]]
    tax_amount: Optional[MoneyDTO]
    total_amount: Optional[MoneyDTO]
    final_amount: Optional[MoneyDTO]
    shipping_reference: Optional[str] = Field(json_schema_extra=AliasChoices('shipping_tracking_reference', 'shipping_reference'))
    coupons: Optional[List[CouponDTO]]
    order_status: enums.OrderStatus
    currency: str
    date_modified: Optional[datetime]
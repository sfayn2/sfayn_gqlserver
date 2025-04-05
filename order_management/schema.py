import graphene
import logging
from dataclasses import asdict
from graphene import relay
from graphene.types.generic import GenericScalar
from ddd.order_management.application import (
    message_bus, dtos, commands, unit_of_work, helpers, queries
  )
from ddd.order_management.domain import enums, exceptions

#logger = logging.getLogger("django")
logger = logging.getLogger(__name__)

# ====================
# Input Types
# ====================
class MoneyInput(graphene.InputObjectType):
    amount = graphene.Float(required=True)
    currency = graphene.String(required=True)

class VendorDetailsInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    country = graphene.String(required=True)

class PackageInput(graphene.InputObjectType):
    weight = graphene.Float(required=True)
    dimensions = graphene.List(graphene.Float, required=True)

class LineItemInput(graphene.InputObjectType):
    product_sku = graphene.String(required=True)
    product_name = graphene.String(required=True)
    vendor = graphene.Field(VendorDetailsInput, required=True)
    product_category = graphene.String(required=True)
    order_quantity = graphene.Int(required=True)
    options = GenericScalar(required=True)
    product_price = graphene.Field(MoneyInput, required=True)
    package = graphene.Field(PackageInput, required=True)

class AddressInput(graphene.InputObjectType):
    street = graphene.String(required=True)
    city = graphene.String(required=True)
    state = graphene.String(required=True)
    postal = graphene.String(required=True)
    country = graphene.String(required=True)

class CustomerDetailsInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)

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


class BaseMutation(relay.ClientIDMutation):
    order = graphene.Field(OrderResponseType)

    command_class = None
    success_message = None
    exception_message = None

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            command = cls.PlaceOrderCommand.model_validate(input)
            order = message_bus.handle(command, unit_of_work.DjangoOrderUnitOfWork())
            #placed order status only in Pending; once payment is confirmed ; webhook will trigger and call api to confirm order
            response_dto = helpers.get_order_response_dto(order, success=True, message=cls.success_message)

        except (exceptions.InvalidOrderOperation, ValueError) as e:
            response_dto = helpers.handle_invalid_order_operation(e)
        except Exception as e:
            response_dto = helpers.handle_unexpected_error(f"{cls.exception_message} {e}")

        return cls(order=OrderResponseType(**response_dto.model_dump()))



# ==========================
# Mutations 
# ===================
class PlaceOrderMutation(BaseMutation):
    class Input:
        order_id = graphene.String()

    command_class = commands.PlaceOrderCommand
    success_message = "Order successfully placed."
    exception_message = "Unexpected error during place order"


# ======
# expected to call in front end via Paypal onApprove ?
# expected to createOrder via paypal.Buttons and make sure to include amount custom_id (internal order_id) 
# ===========

class ConfirmOrderMutation(BaseMutation):
    class Input:
        order_id = graphene.String(required=True) #our own order id
        transaction_id = graphene.String(required=True) #paypal autogenerated order id
        payment_method = graphene.String(required=True)

    command_class = commands.ConfirmOrderCommand
    success_message = "Order successfully confirmed."
    exception_message = "Unexpected error during order confirmation"


class SelectShippingOptionMutation(BaseMutation):
    class Input:
        order_id = graphene.String(required=True)
        shipping_details = graphene.Field(ShippingDetailsInput, required=True)

    command_class = commands.SelectShippingOptionCommand
    success_message = "Order successfully selected shipping option."
    exception_message = "Unexpected error during shipping option selection"


class CheckoutItemsMutation(BaseMutation):
    class Input:
        customer_details = graphene.Field(CustomerDetailsInput, required=True)
        shipping_address = graphene.Field(AddressInput, required=True)
        line_items = graphene.List(LineItemInput, required=True)

    command_class = commands.CheckoutItemsCommand
    success_message = "Cart items successfully checkout."
    exception_message = "Unexpected error during cart items checkout"

# ===========
# Query resolvere here
# ==========
class Query(graphene.ObjectType):

    #shipping_options = graphene.List(ShippingDetailsType)
    shipping_options_by_order_id = graphene.List(ShippingDetailsType, order_id=graphene.String(required=True))
    def resolve_shipping_options_by_order_id(root, info, order_id):
        query = queries.ShippingOptionsQuery(order_id=order_id)
        shipping_options = message_bus.handle(query, unit_of_work.DjangoOrderUnitOfWork())
        response_dto = helpers.get_shipping_options_response_dto(shipping_options)

        return response_dto







import graphene
import logging
from dataclasses import asdict
from graphene import relay
from graphene.types.generic import GenericScalar
from ddd.order_management.application import message_bus, dtos, commands, unit_of_work, helpers
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


# ==========================
# Mutations 
# ===================
class PlaceOrderMutation(relay.ClientIDMutation):
    class Input:
        #order_id = graphene.String()
        customer_details = graphene.Field(CustomerDetailsInput, required=True)
        shipping_address = graphene.Field(AddressInput, required=True)
        line_items = graphene.List(LineItemInput, required=True)
        shipping_details = graphene.Field(ShippingDetailsInput, required=True)
        coupons = graphene.List(CouponInput, required=False)

    order = graphene.Field(OrderResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            command = commands.PlaceOrderCommand.model_validate(input)
            order = message_bus.handle(command, unit_of_work.DjangoOrderUnitOfWork())
            #placed order status only in Pending; once payment is confirmed ; webhook will trigger and call api to confirm order
            response_dto = helpers.get_order_response_dto(order, success=True, message="Order successfully placed.")

        except (exceptions.InvalidOrderOperation, ValueError) as e:
            response_dto = helpers.handle_invalid_order_operation(e)
        except Exception as e:
            response_dto = helpers.handle_unexpected_error(f"Unexpected error during place order {e}")

        return cls(order=OrderResponseType(**response_dto.model_dump()))

# ======
# expected to call in front end via Paypal onApprove ?
# expected to createOrder via paypal.Buttons and make sure to include amount custom_id (internal order_id) 
# ===========

class ConfirmOrderMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True) #our own order id
        transaction_id = graphene.String(required=True) #paypal autogenerated order id
        payment_method = graphene.String(required=True)

    order = graphene.Field(OrderResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            command = commands.ConfirmOrderCommand.model_validate(input)
            order = message_bus.handle(command, unit_of_work.DjangoOrderUnitOfWork())
            response_dto = helpers.get_order_response_dto(order, success=True, message="Order successfully confirmed.")

        except (exceptions.InvalidOrderOperation, ValueError) as e:
            response_dto = helpers.handle_invalid_order_operation(e)
        except Exception as e:
            response_dto = helpers.handle_unexpected_error(f"Unexpected error during confirmation order {e}")

        return cls(order=OrderResponseType(**response_dto.model_dump()))



# ===========
# Sample PlaceOrderMutation
# ======================
"""
mutation {
  placeOrder(input: {
    customerDetails: {
      firstName: "John",
      lastName: "Doe",
      email: "JohnDoe@gmail.com"
    },
    shippingAddress: {
      street: "123 main street",
      city: "New York",
      state: "NYC",
      postal: "1001",
      country: "Singapore"
    },
    lineItems: [
      {
        productSku: "SKU1",
        productName: "Product1",
        vendorDetails {
          name: "Vendor1",
          country: "Singapore"
        },
        productCategory: "Category1",
        orderQuantity: 1,
        options: {color:"red"},
        productPrice: {
          amount: 2.1,
          currency: "SGD"
        },
        package: {
          weight: 1.5,
          dimensions: [10, 10, 10]
        }
      }
    ],
    shippingDetails: {
      method: "Standard",
      deliveryTime: "3-5 business days",
      cost: {
        amount: 5.99,
        currency: "SGD"
      }
    },
    coupons: [{ couponCode: "WELCOME25"}]
  }) {
    order	{
        orderId
    orderStatus
    success
    message
    taxDetails
    offerDetails
    shippingDetails {
      method
      deliveryTime
      cost {
        amount
        currency
      }
    }
    taxAmount {
      amount
      currency
    }
    totalDiscountsFee {
      amount
      currency
    }
    finalAmount {
      amount
      currency
    }
    
    }
  }
}
"""

# ==============
# Sample Confirm Order
# ========
"""
mutation {
  confirmOrder(input: {
    orderId: "ORD-FC8D8D9F",
    transactionId: "2L633961FY072164Y",
    method: "Paypal"
  }) {
    order	{
        orderId
    orderStatus
    success
    message
    taxDetails
    offerDetails
    shippingDetails {
      method
      deliveryTime
      cost {
        amount
        currency
      }
    }
    taxAmount {
      amount
      currency
    }
    totalDiscountsFee {
      amount
      currency
    }
    finalAmount {
      amount
      currency
    }
    
    }
  }
}
"""
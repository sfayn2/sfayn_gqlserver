import graphene
import logging
from dataclasses import asdict
from graphene import relay
from graphene.types.generic import GenericScalar
from ddd.order_management.application import message_bus, dtos, commands, unit_of_work
from ddd.order_management.domain import enums, exceptions
from ddd.order_management.infrastructure import dtos as infra_dtos

#logger = logging.getLogger("django")
logger = logging.getLogger(__name__)

class MoneyInput(graphene.InputObjectType):
    amount = graphene.Float(required=True)
    currency = graphene.String(required=True)

class MoneyType(graphene.ObjectType):
    amount = graphene.Float(required=True)
    currency = graphene.String(required=True)

class PackageInput(graphene.InputObjectType):
    weight = graphene.Float(required=True)
    dimensions = graphene.List(graphene.Float, required=True)

class LineItemInput(graphene.InputObjectType):
    product_sku = graphene.String(required=True)
    product_name = graphene.String(required=True)
    vendor_name = graphene.String(required=True)
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

class CouponInput(graphene.InputObjectType):
    coupon_code = graphene.String(required=True)

class CheckoutOrderMutation(relay.ClientIDMutation):
    class Input:
        customer_details = graphene.Field(CustomerDetailsInput, required=True)
        address = graphene.Field(AddressInput, required=True)
        line_items = graphene.List(LineItemInput, required=True)

    order_id = graphene.String()
    order_status = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try: 
            command = commands.DraftOrderCommand.model_validate(input)

            order = message_bus.handle(command, unit_of_work.DjangoOrderUnitOfWork())

            response_dto = dtos.CheckoutResponseDTO(
                order_id=order.order_id,
                order_status=order.order_status,
                success=True,
                message="Order successfully created."
            )

        except (exceptions.InvalidOrderOperation, ValueError) as e:
            logger.error(f"{e}")
            response_dto = dtos.ResponseWExceptionDTO(
                success=False,
                message=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error during checkout {e}", exc_info=True)
            response_dto = dtos.ResponseWExceptionDTO(
                success=False,
                message="An unexpected error occured. Please contact support."
            )

        return cls(**response_dto.model_dump())

class PlaceOrderMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String()
        customer_details = graphene.Field(CustomerDetailsInput, required=True)
        shipping_address = graphene.Field(AddressInput, required=True)
        line_items = graphene.List(LineItemInput, required=True)
        shipping_details = graphene.Field(ShippingDetailsInput, required=True)
        coupons = graphene.List(CouponInput, required=False)

    order_id = graphene.String()
    order_status = graphene.String()
    success = graphene.String()
    message = graphene.String()
    tax_details = graphene.List(graphene.String)
    offer_details = graphene.List(graphene.String)
    tax_amount  = graphene.Field(MoneyType)
    total_discounts_fee = graphene.Field(MoneyType)
    final_amount = graphene.Field(MoneyType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            command = commands.PlaceOrderCommand.model_validate(input)

            order = message_bus.handle(command, unit_of_work.DjangoOrderUnitOfWork())

            #placed order status only in Pending; once payment is confirmed ; webhook will trigger and call api to confirm order
            response_dto = dtos.PlaceOrderResponseDTO(
                order_id=order.order_id,
                order_status=order.order_status,
                success=True,
                message="Order successfully placed.",
                tax_details=order.tax_details,
                offer_details=order.offer_details,
                tax_amount=asdict(order.tax_amount),
                total_discounts_fee=asdict(order.total_discounts_fee),
                final_amount=asdict(order.final_amount)
            )

        except (exceptions.InvalidOrderOperation, ValueError) as e:
            logger.error(f"{e}")
            response_dto = dtos.ResponseWExceptionDTO(
                success=False,
                message=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error during place order {e}", exc_info=True)
            response_dto = dtos.ResponseWExceptionDTO(
                success=False,
                message="An unexpected error occured. Please contact support."
            )


        return cls(**response_dto.model_dump())



"""
Sample CheckOrderMutation mutation

mutation {
  checkoutOrder(input: {
    customerDetails: {
      firstName: "John",
      lastName: "Doe",
      email: "JohnDoe@gmail.com"
    },
    address: {
      street: "123 main street",
      city: "New York",
      state: "NYC",
      postal: "1001",
      country: "USA"
    },
    lineItems: [
      {
        productSku: "SKU1",
        productName: "Product1",
        vendorName: "Vendor1",
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
    ]
  }) {
    orderId
    orderStatus
    success
    message
  }
}
"""

"""
Sample PlaceOrderMutation mutation

mutation {
  placeOrder(input: {
    orderId: "ORD-CAB3E0E2"
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
      country: "USA"
    },
    lineItems: [
      {
        productSku: "SKU1",
        productName: "Product1",
        vendorName: "Vendor1",
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
    coupons: [{ couponCode:"WELCOME25"}]
  }) {
    orderId
    orderStatus
    success
    message
    taxDetails
    offerDetails
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
"""
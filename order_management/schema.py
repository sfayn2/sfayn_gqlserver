import graphene
from graphene import relay
from graphene.types.generic import GenericScalar
from ddd.order_management.application import message_bus, dtos, commands, unit_of_work
from ddd.order_management.domain import enums

class MoneyInput(graphene.InputObjectType):
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

class CheckoutOrderMutation(relay.ClientIDMutation):
    class Input:
        customer_details = graphene.Field(CustomerDetailsInput, required=True)
        address = graphene.Field(AddressInput, required=True)
        line_items = graphene.List(LineItemInput, required=True)

    order_id = graphene.String()
    order_status = graphene.String()
    message = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        request_dto = dtos.CheckoutRequestDTO.model_validate(input)

        command = commands.CheckoutCommand(
            customer_details=request_dto.customer_details,
            address=request_dto.address,
            line_items=request_dto.line_items
        )

        order = message_bus.handle(command, unit_of_work.DjangoUnitOfWork())

        response_dto = dtos.CheckoutResponseDTO(
            order_id=order.order_id,
            order_status=order.order_status,
            message="Order successfully created."
        )

        return cls(**response_dto.model_dump())

"""
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
    message
  }
}
"""
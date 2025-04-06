import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, commands, unit_of_work, queries
  )
from ddd.order_management.domain import exceptions
from ddd.order_management.presentation.graphql import object_types, input_types, common, factories
from ddd.order_management.infrastructure.adapters import payments_adapter

# ==========================
# Mutations 
# ===================
class PlaceOrderMutation(common.BaseOrderMutation):
    class Input:
        order_id = graphene.String()

    command_class = commands.PlaceOrderCommand
    success_message = "Order successfully placed."
    exception_message = "Unexpected error during place order"


# ======
# expected to call in front end via Paypal onApprove ?
# expected to createOrder via paypal.Buttons and make sure to include amount custom_id (internal order_id) 
# ===========

class ConfirmOrderMutation(relay.ClientIDMutation):
    class Input:
        order_id = graphene.String(required=True) #our own order id
        transaction_id = graphene.String(required=True) #paypal autogenerated order id
        payment_method = graphene.String(required=True)

    order = graphene.Field(object_types.OrderResponseType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        try:
            command = commands.ConfirmOrderCommand.model_validate(input)
            payment_gateway_factory = payments_adapter.PaymentGatewayFactory(command.payment_method)
            order = message_bus.handle(
                    command, 
                    unit_of_work.DjangoOrderUnitOfWork(), 
                    dependencies={"payment_gateway_factory": payment_gateway_factory}
                )

            #placed order status only in Pending; once payment is confirmed ; webhook will trigger and call api to confirm order
            response_dto = common.get_order_response_dto(order, success=True, message="Order successfully confirmed.")

        except (exceptions.InvalidOrderOperation, ValueError) as e:
            response_dto = common.handle_invalid_order_operation(e)
        except Exception as e:
            response_dto = common.handle_unexpected_error(f"Unexpected error during order confirmation {e}")

        return cls(order=object_types.OrderResponseType(**response_dto.model_dump()))



class SelectShippingOptionMutation(common.BaseOrderMutation):
    class Input:
        order_id = graphene.String(required=True)
        shipping_details = graphene.Field(input_types.ShippingDetailsInput, required=True)

    command_class = commands.SelectShippingOptionCommand
    success_message = "Order successfully selected shipping option."
    exception_message = "Unexpected error during shipping option selection"


class CheckoutItemsMutation(common.BaseOrderMutation):
    class Input:
        customer_details = graphene.Field(input_types.CustomerDetailsInput, required=True)
        shipping_address = graphene.Field(input_types.AddressInput, required=True)
        line_items = graphene.List(input_types.LineItemInput, required=True)

    command_class = commands.CheckoutItemsCommand
    success_message = "Cart items successfully checkout."
    exception_message = "Unexpected error during cart items checkout"

# ===========
# Query resolvere here
# ==========
class Query(graphene.ObjectType):

    #shipping_options = graphene.List(ShippingDetailsType)
    shipping_options_by_order_id = graphene.List(input_types.ShippingDetailsType, order_id=graphene.String(required=True))
    def resolve_shipping_options_by_order_id(root, info, order_id):
        query = queries.ShippingOptionsQuery(order_id=order_id)
        shipping_options = message_bus.handle(query, unit_of_work.DjangoOrderUnitOfWork())
        response_dto = common.get_shipping_options_response_dto(shipping_options)

        return response_dto







import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, queries
  )
from ddd.order_management.presentation.graphql import object_types, input_types, common
from ddd.order_management.infrastructure import (
    access_control1,
)

class ListCustomerAddressesQuery(graphene.ObjectType):

    list_customer_addresses_by_customer_id = graphene.List(object_types.AddressType, customer_id=graphene.String(required=True))
    def resolve_list_customer_addresses_by_customer_id(root, info, customer_id):
        token = common.get_token_from_context(info)
        user_ctx = access_control1.get_user_context(token)
        query = queries.ListCustomerAddressesQuery(customer_id=customer_id)
        customer_addresses = message_bus.handle(query, user_ctx=user_ctx)

        return customer_addresses
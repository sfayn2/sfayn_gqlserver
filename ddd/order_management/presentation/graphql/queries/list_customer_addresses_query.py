import graphene
from graphene import relay
from ddd.order_management.application import (
    message_bus, queries
  )
from ddd.order_management.presentation.graphql import object_types, input_types

class ListCustomerAddressesQuery(graphene.ObjectType):

    list_customer_addresses_by_customer_id = graphene.List(object_types.AddressType, customer_id=graphene.String(required=True))
    def resolve_list_customer_addresses_by_customer_id(root, info, customer_id):
        query = queries.ListCustomerAddressesQuery(customer_id=customer_id)
        customer_addresses = message_bus.handle(query)

        return customer_addresses
import graphene
import product_catalog.schema
import ddd.order_management.presentation.graphql.mutations
import ddd.order_management.presentation.graphql.mutations.checkout_items_mutation
import ddd.order_management.presentation.graphql.mutations.confirm_order_mutation
import ddd.order_management.presentation.graphql.mutations.place_order_mutation
import ddd.order_management.presentation.graphql.mutations.select_shipping_option_mutation
import ddd.order_management.presentation.graphql.queries
import ddd.order_management.presentation.graphql.queries.shipping_options_query
import ddd.order_management.presentation.graphql.schema
from ddd.order_management.presentation.graphql import queries


class Query(
    product_catalog.schema.Query,
    ddd.order_management.presentation.graphql.queries.ShippingOptionsQuery
):
    #This class will inherit from multiple queries
    #as we begin to add more apps to our project
    pass

class Mutation(graphene.ObjectType):
    checkout_items = ddd.order_management.presentation.graphql.mutations.checkout_items_mutation.CheckoutItemsMutation.Field()
    place_order = ddd.order_management.presentation.graphql.mutations.place_order_mutation.PlaceOrderMutation.Field()
    confirm_order = ddd.order_management.presentation.graphql.mutations.confirm_order_mutation.ConfirmOrderMutation.Field()
    select_shipping_option = ddd.order_management.presentation.graphql.mutations.select_shipping_option_mutation.SelectShippingOptionMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


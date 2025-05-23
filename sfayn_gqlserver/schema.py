import graphene
import product_catalog.schema
from ddd.order_management.presentation.graphql import queries, mutations



class Query(
    product_catalog.schema.Query,
    queries.ShippingOptionsQuery
):
    pass

class Mutation(graphene.ObjectType):
    checkout_items = mutations.checkout_items_mutation.CheckoutItemsMutation.Field()
    place_order = mutations.place_order_mutation.PlaceOrderMutation.Field()
    confirm_order = mutations.confirm_order_mutation.ConfirmOrderMutation.Field()
    select_shipping_option = mutations.select_shipping_option_mutation.SelectShippingOptionMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


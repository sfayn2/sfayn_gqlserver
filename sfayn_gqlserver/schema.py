import graphene
import product_catalog.schema
import ddd.order_management.interfaces.graphql.schema

class Query(
    product_catalog.schema.Query,
    ddd.order_management.interfaces.graphql.schema.Query
):
    #This class will inherit from multiple queries
    #as we begin to add more apps to our project
    pass

class Mutation(graphene.ObjectType):
    checkout_items = ddd.order_management.interfaces.graphql.schema.CheckoutItemsMutation.Field()
    place_order = ddd.order_management.interfaces.graphql.schema.PlaceOrderMutation.Field()
    confirm_order = ddd.order_management.interfaces.graphql.schema.ConfirmOrderMutation.Field()
    select_shipping_option = ddd.order_management.interfaces.graphql.schema.SelectShippingOptionMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


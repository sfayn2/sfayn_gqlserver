import graphene
import product_catalog.schema
import order_management.schema

class Query(
    product_catalog.schema.Query
):
    #This class will inherit from multiple queries
    #as we begin to add more apps to our project
    pass

class Mutation(graphene.ObjectType):
    checkout_order = order_management.schema.CheckoutOrderMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


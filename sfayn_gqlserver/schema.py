import graphene
import product_catalog.schema

class Query(
    product_catalog.schema.Query
):
    #This class will inherit from multiple queries
    #as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)


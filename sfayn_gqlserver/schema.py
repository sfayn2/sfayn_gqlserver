import graphene
import graphql_jwt

import cb.schema
import product.schema
import shop.schema

class Query(product.schema.Query, shop.schema.Query, graphene.ObjectType):
    #This class will inherit from multiple queries
    #as we begin to add more apps to our project
    pass

class Mutation(graphene.ObjectType):
    shopcart = shop.schema.ShopCartMutation.Field()
#    shopping_cart = cb.schema.ShoppingCartMutation.Field()
#    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
#    verify_token = graphql_jwt.Verify.Field()
#    refresh_token = graphql_jwt.Refresh.Field()
#
schema = graphene.Schema(query=Query, mutation=Mutation)


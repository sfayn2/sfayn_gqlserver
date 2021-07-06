import graphene
import graphql_jwt

import cb.schema
import product.schema
import shop.schema
import customer.schema
import account.schema
import payment.schema

class Query(
    product.schema.Query, 
    shop.schema.Query, 
    customer.schema.Query,
    account.schema.Query,
    payment.schema.Query,
    graphene.ObjectType
):
    #This class will inherit from multiple queries
    #as we begin to add more apps to our project
    pass

class Mutation(graphene.ObjectType):
    shopcart = shop.schema.ShopCartMutation.Field()
    shoporder = shop.schema.ShopOrderMutation.Field()
    shoporderitem = shop.schema.ShopOrderItemMutation.Field()
    shoporderstatus = shop.schema.ShopOrderStatusMutation.Field()
#    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
#    verify_token = graphql_jwt.Verify.Field()
#    refresh_token = graphql_jwt.Refresh.Field()
#
schema = graphene.Schema(query=Query, mutation=Mutation)


import graphene
import graphql_jwt

import product.schema
import order.schema
import tag.schema
import discount.schema
import accounts.schema
import payment.schema

class Query(
    product.schema.Query, 
    shop.schema.Query, 
    order.schema.Query, 
    tag.schema.Query, 
    discount.schema.Query, 
    accounts.schema.Query,
    payment.schema.Query,
    graphene.ObjectType
):
    #This class will inherit from multiple queries
    #as we begin to add more apps to our project
    pass

class Mutation(graphene.ObjectType):

    orderitem = order.schema.OrderItemMutation.Field()
    orderstatus = order.schema.OrderStatusMutation.Field()
    order = order.schema.OrderMutation.Field() #make sure it at last so wont override order model w. order mutation

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
#
schema = graphene.Schema(query=Query, mutation=Mutation)


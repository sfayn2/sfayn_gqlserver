
from cb.models import ShoppingCart, WAREHOUSE_CHOICES
from django.db.models import Count
from graphql_relay import from_global_id
from django.db.models import Min, Max
from product.models import ProductVariantItem

def get_shoppingcart_total_count(user_id):
    return ShoppingCart.objects.filter(user_id=user_id).count()

def get_list_from_global_id(data):
    final_id = []
    for d in data.split(","):
        #need to convert graphene relay id to db id
        final_id.append(from_global_id(d)[1]) 
    return final_id


def get_price_min(id):
    qset = ProductVariantItem.objects.filter(parent_sn_id=id)
    return qset.aggregate(Min("price"))["price__min"]

def get_price_max(id):
    qset = ProductVariantItem.objects.filter(parent_sn_id=id)
    return qset.aggregate(Max("price"))["price__max"]



    

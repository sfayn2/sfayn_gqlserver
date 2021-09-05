
from cb.models import ShoppingCart, WAREHOUSE_CHOICES
from django.db.models import Count
from graphql_relay import from_global_id
from django.db.models import Min, Max
from product.models import (
    ProductVariantItem,
    ProductCategory
)

def get_shoppingcart_total_count(user_id):
    return ShoppingCart.objects.filter(user_id=user_id).count()

def get_list_from_global_id(data):
    final_id = []
    for d in data:
        #need to convert graphene relay id to db id
        final_id.append(from_global_id(d)[1]) 
    return final_id


def get_price_min(id):
    qset = ProductVariantItem.objects.filter(parent_sn_id=id)
    return qset.aggregate(Min("price"))["price__min"]

def get_price_max(id):
    qset = ProductVariantItem.objects.filter(parent_sn_id=id)
    return qset.aggregate(Max("price"))["price__max"]

def get_l3_categories(category_id_list, level):

    category = ProductCategory
    category_qset = category.objects.all()
    l3_categories = None

    if  category.LevelChoices.LEVEL_1 == level:
        l2_categories = list(
            category_qset.filter(
                parent_id__in=category_id_list
            ).values_list('id', flat=True)
        )

        l3_categories = list(
            category_qset.filter(
                parent_id__in=l2_categories
            ).values_list('id', flat=True)
        )


    elif  category.LevelChoices.LEVEL_2 == level:
        l3_categories = list(
            category_qset.filter(
                parent_id__in=category_id_list
            ).values_list('id', flat=True)
        )


    return l3_categories



    

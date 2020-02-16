
from cb.models import ShoppingCart
from django.db.models import Count

def get_shoppingcart_total_count(user_id):
    return ShoppingCart.objects.filter(user_id=user_id).count()


def get_shoppingcart_group_by_warehouse():
    
    warehouse_names_list = list(ShoppingCart.objects.values('product__warehouse__warehouse').annotate(warehouse_count=Count('product__warehouse__warehouse')))

    wname_shopcart = []
    for name in warehouse_names_list:
        temp = {}
        temp['name'] = name['product__warehouse__warehouse']
        temp['shopping_cart'] = ShoppingCart.objects.filter(product__warehouse__warehouse=temp['name'])
        wname_shopcart.append(temp)

        print (wname_shopcart)

        return [   {  "warehouses": wname_shopcart  }   ]

    return []




    


from cb.models import ShoppingCart
from django.db.models import Count

def get_shoppingcart_total_count(user_id):
    return ShoppingCart.objects.filter(user_id=user_id).count()


def get_shoppingcart_group_by_warehouse():
    
    warehouse_original_list = list(
        ShoppingCart.objects.values('product__warehouse__warehouse').annotate(
            warehouse_count=Count('product__warehouse__warehouse')
        )
    )

    final_warehouse = []
    total_count = 0

    for name in warehouse_original_list:

        temp = {}
        temp['name'] = name['product__warehouse__warehouse']
        temp['shopping_cart'] = ShoppingCart.objects.filter(
            product__warehouse__warehouse=temp['name']
        )

        final_warehouse.append(temp)
        total_count += 1

    return [{ "warehouses": final_warehouse, 
              "totalCount": total_count  } ]





    

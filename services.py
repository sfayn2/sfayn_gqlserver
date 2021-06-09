
from cb.models import ShoppingCart, WAREHOUSE_CHOICES
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
    warehouse_dict = dict(WAREHOUSE_CHOICES)

    for name in warehouse_original_list:

        temp = {}
        temp['name'] = warehouse_dict[name['product__warehouse__warehouse']]
        temp['shopping_cart'] = ShoppingCart.objects.filter(
            product__warehouse__warehouse=name['product__warehouse__warehouse']
        )

        if temp["shopping_cart"].exists():
            total_count += temp['shopping_cart'].count()

        final_warehouse.append(temp)

    return [{ "warehouses": final_warehouse, 
              "total_count": total_count  } ]





    

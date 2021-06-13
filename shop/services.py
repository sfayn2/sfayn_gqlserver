from .models import ShopCart
from django.db.models import Count

def get_shopcart_group_by_owner():
    
    owner_list = list(
        ShopCart.objects.values('product_variant__parent_sn__created_by').annotate(
            owner_count_count=Count('product_variant__parent_sn__created_by')
        )
    )

    import pdb; pdb.set_trace()

    final_owner = []
    total_count = 0

    for name in owner_list:

        temp = {}
        temp['owner'] = warehouse_dict[name['product_variant__parent_sn__created_by']]
        temp['shopcart'] = ShoppingCart.objects.filter(
            product__warehouse__warehouse=name['product_variant__parent_sn__created_by']
        )

        if temp["shopcart"].exists():
            total_count += temp['shopcart'].count()

        final_owner.append(temp)

    return [{ "owner": final_owner, 
              "total_count": total_count  } ]





    

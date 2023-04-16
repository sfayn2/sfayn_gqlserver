from django.contrib import admin
from .models import (
    ShopCart,
    ShopOrder,
    ShopOrderItem,
    ShopProfile
)

# Register your models here.
class ShopProfileAdmin(admin.ModelAdmin):
    #filter_horizontal = ('promotional_banner', 'category', 'product')
    filter_horizontal = ('promotional_banner', 'product')
    search_fields = ("name", "domain")
    list_display = ("id", "domain", "name", "shop_desc", "group_id", "created_by_id")
    list_display_links = ("domain", "name",)

    def name(self, obj):
        return obj.site.name

#TODO to obsolte
class ShopCartAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "product_variant", "quantity")
    list_display_links = ("product_variant",)

    def title(self, obj):
        return obj.product_variant.parent_sn.title


#TODO to obsolte
class ShopOrderAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "payment_method", "customer_address", )
    list_display_links = ("payment_method", "customer_address")


#TODO to obsolte
class ShopOrderItemAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "order_id", "shopcart")
    list_display_links = ("shopcart",)


#TODO to obsolte
admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(ShopOrder, ShopOrderAdmin)
admin.site.register(ShopOrderItem, ShopOrderItemAdmin)


admin.site.register(ShopProfile, ShopProfileAdmin)

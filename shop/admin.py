from django.contrib import admin
from .models import (
    ShopCart,
    ShopOrder,
    ShopOrderItem
)

# Register your models here.
class ShopCartAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "product_variant", "quantity")
    list_display_links = ("product_variant",)

    def title(self, obj):
        return obj.product_variant.parent_sn.title


class ShopOrderAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "payment_method", "customer_address", )
    list_display_links = ("payment_method", "customer_address")


class ShopOrderItemAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "order_id", "shopcart")
    list_display_links = ("shopcart",)


admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(ShopOrder, ShopOrderAdmin)
admin.site.register(ShopOrderItem, ShopOrderItemAdmin)

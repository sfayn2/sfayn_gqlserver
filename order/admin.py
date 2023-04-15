from django.contrib import admin
from .models import (
    Order,
    OrderItem
)

class OrderAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "payment_method", "customer_address", )
    list_display_links = ("payment_method", "customer_address")


class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "order_id", "product_variant_id")
    list_display_links = ("product_variant_id",)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

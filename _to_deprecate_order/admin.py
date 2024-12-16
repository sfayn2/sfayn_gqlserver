from django.contrib import admin
from common import (
        CommonAdmin,
        get_list_display)
from .models import (
    Order,
    OrderItem
)

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(CommonAdmin):
    search_fields = ("created_by",)
    #list_display = ("id", "payment_method", "shipping_address", "tax", "shipping_fee", "discount_fee", "tax_rate", "total_amount", "notes", "status", "created_by", "date_created", "date_modified")
    list_display = get_list_display(Order, ("order2orderitem", ))
    #list_display_links = ("shipping_address",)

    inlines = [
        OrderItemInline,
    ]


admin.site.register(Order, OrderAdmin)

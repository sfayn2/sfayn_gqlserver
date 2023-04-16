from django.contrib import admin
from .models import (
    Order,
    OrderItem
)

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "payment_method", "customer_address", )
    list_display_links = ("payment_method", "customer_address")

    inlines = [
        OrderItemInline,
    ]


admin.site.register(Order, OrderAdmin)

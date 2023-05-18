from django.contrib import admin
from .models import (
    Discount,
)


class DiscountAdmin(admin.ModelAdmin):
    filter_horizontal = ('vendor', 'tag', 'product_variant', 'category', 'shipping_method')
    search_fields = ("created_by",)
    list_display = ("id", "name", "discount_type", "is_enable")
    list_display_links = ("name", )

admin.site.register(Discount, DiscountAdmin)

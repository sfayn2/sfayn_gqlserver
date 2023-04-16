from django.contrib import admin
from .models import (
    Discount,
    DiscountTypePercentage,
    DiscountTypeBuyXGetX
)

class DiscountTypePercentageAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "name", "minimum_quantity", "discount_percentage", "start_date", "end_date", "created_by")
    list_display_links = ("name", )


class DiscountTypeBuyXGetXAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "name", "buy_quantity", "get_quantity", "start_date", "end_date", "created_by")
    list_display_links = ("name", )

class DiscountAdmin(admin.ModelAdmin):
    filter_horizontal = ('shop', 'tag', 'product_variant', 'category')
    search_fields = ("created_by",)
    list_display = ("id", "name", "discount_type", "status")
    list_display_links = ("name", )

admin.site.register(Discount, DiscountAdmin)
admin.site.register(DiscountTypePercentage, DiscountTypePercentageAdmin)
admin.site.register(DiscountTypeBuyXGetX, DiscountTypeBuyXGetXAdmin)

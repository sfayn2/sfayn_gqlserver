from django.contrib import admin
from .models import (
    Discount,
    DiscountTypePercentageOrFixAmount,
    DiscountTypeBuyXGetX,
    DiscountTypeVoucher
)

class DiscountTypePercentageOrFixAmountAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "name", "minimum_quantity", "by_percentage", "fix_amount", "start_date", "end_date", "created_by")
    list_display_links = ("name", )


class DiscountTypeBuyXGetXAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "name", "buy_quantity", "get_quantity", "start_date", "end_date", "created_by")
    list_display_links = ("name", )


class DiscountTypeVoucherAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "name", "voucher", "percent_offer", "fix_offer", "min_spend", "capped_at", "free_shipping", "usage_limit", "created_by")
    list_display_links = ("name", )

class DiscountAdmin(admin.ModelAdmin):
    filter_horizontal = ('vendor', 'tag', 'product_variant', 'category', 'shipping_method')
    search_fields = ("created_by",)
    list_display = ("id", "name", "discount_type", "is_enable")
    list_display_links = ("name", )

admin.site.register(Discount, DiscountAdmin)
admin.site.register(DiscountTypePercentageOrFixAmount, DiscountTypePercentageOrFixAmountAdmin)
admin.site.register(DiscountTypeBuyXGetX, DiscountTypeBuyXGetXAdmin)
admin.site.register(DiscountTypeVoucher, DiscountTypeVoucherAdmin)

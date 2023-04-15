from django.contrib import admin
from .models import (
    Discount,
)

class DiscountAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "name", "discount_price", "discount_percentage", "start_date", "end_date", "status")
    list_display_links = ("name", )

admin.site.register(Discount, DiscountAdmin)

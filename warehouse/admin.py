from django.contrib import admin
from .models import Stock
from product.models import VariantItem
from common import (
        CommonAdmin,
        get_list_display)

# Register your models here.
class StockAdmin(CommonAdmin):
    search_fields = ("stock", "price",)
    autocomplete_fields = ["product_variant"]
    list_display_links = ("warehouse",)
    list_display = get_list_display(Stock, ("warehouse2stock",)) 


#admin.site.register(Stock, StockAdmin)

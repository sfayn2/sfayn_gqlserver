from django.contrib import admin
from .models import Warehouse, Stock
from product.models import ProductVariantItem
from services import CommonAdmin

# Register your models here.
class WarehouseAdmin(CommonAdmin):
    search_fields = ("name", "address", "country", "region")
    list_display_links = ("name",)
    list_display = ("name", "address", "postal", "country", "region", "handling_fee", "status", "created_by", "date_created", "date_modified")


class StockAdmin(CommonAdmin):
    search_fields = ("stock", "price",)
    autocomplete_fields = ["product_variant"]
    list_display_links = ("get_product_title",)
    list_display = ("get_warehouse_name", "get_product_title", "stock", "price", "status", "created_by", "date_created", "date_modified")

    def get_warehouse_name(self, obj):
        return obj.warehouse.name


    def get_product_title(self, obj):
        return obj.product_variant.parent_sn.title

    get_warehouse_name.short_description = "Warehouse Name"
    get_product_title.short_description = "Product Title" 
    


admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Stock, StockAdmin)

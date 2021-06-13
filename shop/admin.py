from django.contrib import admin
from .models import ShopCart

# Register your models here.
class ShopCartAdmin(admin.ModelAdmin):
    search_fields = ("created_by",)
    list_display = ("id", "quantity", "created_by", "product_variant_id", "title")

    def title(self, obj):
        return obj.product_variant.parent_sn.title

admin.site.register(ShopCart, ShopCartAdmin)

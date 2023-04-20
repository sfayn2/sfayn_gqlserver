from django.contrib import admin
from services import CommonAdmin
from .models import (
    ShopProfile
)


# Register your models here.
class ShopProfileAdmin(CommonAdmin):
    filter_horizontal = ('product',)
    search_fields = ("name", "domain")
    list_display_links = ("domain", "name",)
    list_display = ("name", "domain", "shop_desc", "get_groups", "get_products", "created_by", "date_created", "date_modified")

    def get_groups(self, obj):
        if obj.group:
            return " | ".join([str(p) for p in obj.group.all()])
        else:
            return None

    def get_products(self, obj):
        if obj.product:
            return " | ".join([str(p) for p in obj.product.all()])
        else:
            return None

    get_groups.short_description = "Group owner of this Shop"
    get_products.short_description = "Products owned by this Shop"
    


admin.site.register(ShopProfile, ShopProfileAdmin)

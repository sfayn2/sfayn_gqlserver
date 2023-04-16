from django.contrib import admin
from .models import (
    ShopProfile
)


# Register your models here.
class ShopProfileAdmin(admin.ModelAdmin):
    #filter_horizontal = ('promotional_banner', 'category', 'product')
    filter_horizontal = ('product',)
    search_fields = ("name", "domain")
    list_display = ("id", "domain", "name", "shop_desc", "group_id", "created_by_id")
    list_display_links = ("domain", "name",)

    def name(self, obj):
        return obj.site.name


admin.site.register(ShopProfile, ShopProfileAdmin)

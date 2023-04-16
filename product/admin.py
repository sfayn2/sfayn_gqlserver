from django.contrib import admin
from django.conf import settings
from .models import (
    ProductParent,
    ProductCategory,
    ProductVariantItem,
)

class ProductVariantItemInline(admin.TabularInline):
        model = ProductVariantItem


# Register your models here.
class ProductParentAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("parent_sn", "title")
    list_display_links = ("title",)

    inlines = [
        ProductVariantItemInline,
    ]


class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "level", "parent_name", "name")

    @admin.display(empty_value="Not applicable")
    def parent_name(self, obj):
        try:
            return obj.parent.name
        except:
            return obj.parent




admin.site.register(ProductParent, ProductParentAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)

admin.site.site_url = settings.VIEW_SITE_URL
admin.site.site_header = 'Sfayn Settings'    

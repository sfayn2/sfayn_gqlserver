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



class ProductVariantItemAdmin(admin.ModelAdmin):
    search_fields = ("sku", "parent_sn__title")
    list_display = ("id", "product_variant", "get_product_title", "sku", "quantity", "price", "options", "img_url", "default", "created_by", "date_created", "date_modified")
    list_display_links = ("get_product_title",)


    def get_product_title(self, obj):
        return obj.parent_sn.title

    get_product_title.short_description = "Product Title" 


admin.site.register(ProductParent, ProductParentAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductVariantItem, ProductVariantItemAdmin)

admin.site.site_url = settings.VIEW_SITE_URL
admin.site.site_header = 'Sfayn Settings'    

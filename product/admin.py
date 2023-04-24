from django.contrib import admin
from .models import (
    Product,
    Category,
    VariantItem,
)

class VariantItemInline(admin.TabularInline):
        model = VariantItem


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("product_sn", "title")
    list_display_links = ("title",)

    inlines = [
        VariantItemInline,
    ]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "level", "parent_name", "name")

    @admin.display(empty_value="Not applicable")
    def parent_name(self, obj):
        try:
            return obj.parent.name
        except:
            return obj.parent



class VariantItemAdmin(admin.ModelAdmin):
    search_fields = ("sku", "product_sn__title")
    list_display = ("id", "product_variant", "get_product_title", "sku", "quantity", "price", "options", "img_url", "default", "created_by", "date_created", "date_modified")
    list_display_links = ("get_product_title",)


    def get_product_title(self, obj):
        return obj.product_sn.title

    get_product_title.short_description = "Product Title" 


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(VariantItem, VariantItemAdmin)


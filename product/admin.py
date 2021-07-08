from django.contrib import admin
from .models import (
    ProductParent,
    ProductVariant,
    ProductVideo,
    ProductImage,
    ProductCategory
)

# Register your models here.
class ProductParentAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("parent_sn", "title")
    list_display_links = ("title",)


class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("level", "parent_name", "name")

    @admin.display(empty_value="Not applicable")
    def parent_name(self, obj):
        try:
            return obj.parent.name
        except:
            return obj.parent


class ProductVariantAdmin(admin.ModelAdmin):
    search_fields = ("sku",)
    list_display = ("sku", "parent_sn", "quantity", "price", "name", "options")


class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ("parent_sn",)
    list_display = ("parent_sn", "img_url", "cover_photo")


class ProductVideoAdmin(admin.ModelAdmin):
    search_fields = ("parent_sn",)
    list_display = ("parent_sn", "video_url")


admin.site.register(ProductParent, ProductParentAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductVideo, ProductVideoAdmin)

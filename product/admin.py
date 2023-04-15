from django.contrib import admin
from django.conf import settings
from .models import (
    ProductParent,
    ProductVideo,
    ProductImage,
    ProductCategory,
    ProductTag,
    ProductTagItem,
    ProductVariant,
    ProductVariantItem,
)

# Register your models here.
class ProductParentAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("parent_sn", "title", "shop")
    list_display_links = ("title",)

    def shop(self, obj):
        return obj.shop.name


class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("id", "level", "parent_name", "name")

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


class ProductTagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", )


class ProductTagItemAdmin(admin.ModelAdmin):
    search_fields = ("product_tag",)
    list_display = ("product_tag", "product_variant")


class ProductVariantAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", )


class ProductVariantItemAdmin(admin.ModelAdmin):
    search_fields = ("sku",)
    list_display = ("product_variant", "options", "sku", "parent_sn", "quantity", "price")
    list_display_links = ("sku", )


admin.site.register(ProductParent, ProductParentAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductVideo, ProductVideoAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
admin.site.register(ProductTagItem, ProductTagItemAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductVariantItem, ProductVariantItemAdmin)

admin.site.site_url = settings.VIEW_SITE_URL
admin.site.site_header = 'Sfayn Settings'    

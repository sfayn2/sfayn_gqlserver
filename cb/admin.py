from django.contrib import admin
from .models import Product, ProductWarehouse, ProductOriginalImg, ProductDescImg

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('sku', 'title', 'color', 'size')
    list_display_links = ('title',)


class ProductWarehouseAdmin(admin.ModelAdmin):
    search_fields = ('warehouse',)
    list_display = ('product__sku', 'product__title', 'warehouse', 'price', 'url',)
    list_display_links = ('product__title',)

    def product__sku(self, obj):
        return obj.product.sku

    def product__title(self, obj):
        return obj.product.title


class ProductOriginalImgAdmin(admin.ModelAdmin):
    search_fields = ('original_img',)
    list_display = ('product__sku', 'product__title', 'original_img',)
    list_display_links = ('product__title',)

    def product__sku(self, obj):
        return obj.product.sku

    def product__title(self, obj):
        return obj.product.title


class ProductDescImgAdmin(admin.ModelAdmin):
    search_fields = ('desc_img',)
    list_display = ('product__sku', 'product__title', 'desc_img',)
    list_display_links = ('product__title',)

    def product__sku(self, obj):
        return obj.product.sku

    def product__title(self, obj):
        return obj.product.title

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductWarehouse, ProductWarehouseAdmin)
admin.site.register(ProductOriginalImg, ProductOriginalImgAdmin)
admin.site.register(ProductDescImg, ProductDescImgAdmin)

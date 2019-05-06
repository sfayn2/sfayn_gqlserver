from django.contrib import admin
from .models import Product, ProductWarehouse, ProductOriginalImg, ProductDescImg, ProductCategory

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('product__parent_sn', 'sku', 'title', 'color', 'size')
    list_display_links = ('title',)

    def product__parent_sn(self, obj):
        return obj.parent_sn.parent_sn


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
    list_display = ('id', 'product__sku', 'product__title', 'original_img',)
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

class ProductCategoryAdmin(admin.ModelAdmin):
    search_fields = ('cat_name',)
    list_display = ('parent_id', 'cat_id', 'cat_name',)

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductWarehouse, ProductWarehouseAdmin)
admin.site.register(ProductOriginalImg, ProductOriginalImgAdmin)
admin.site.register(ProductDescImg, ProductDescImgAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)

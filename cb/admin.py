from django.contrib import admin
from .models import Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('sku', 'title', 'color', 'size')
    list_display_links = ('title',)


# Register your models here.
admin.site.register(Product, ProductAdmin)

from django.contrib import admin
from common import (
        CommonAdmin, 
        get_list_display)
from .models import (
    Product,
    Category,
    VariantItem,
    Variant
)

class VariantItemInline(admin.TabularInline):
        model = VariantItem


# Register your models here.
class ProductAdmin(CommonAdmin):
    search_fields = ("title",)
    list_display_links = ("title",)
    list_display = get_list_display(Product, ("product2variantitem",))
    inlines = (VariantItemInline,)

    readonly_fields = ["created_by", "status"]
    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        #obj.status = 1 > cn overried depends on the settings? use function so can reuse in schema.py
        super().save_model(request, obj, form, change)



class CategoryAdmin(CommonAdmin):
    search_fields = ("name",)
    list_display_links = ("name",)
    list_display = get_list_display(Category, ("cat2product", "category2discount", "category"))

    @admin.display(empty_value="Not applicable")
    def parent_name(self, obj):
        try:
            return obj.parent.name
        except:
            return obj.parent



class VariantItemAdmin(CommonAdmin):
    search_fields = ("sku", "product_sn__title")
    list_display = get_list_display(VariantItem, ("variant2tags", "prodvariant2stock", "prodvariant2discount", "prodvariant2orderitem", )) 
    list_display_links = ("get_product_title",)
    list_display.insert(1 ,"get_product_title") #insert in second position



    def get_product_title(self, obj):
        return obj.product_sn.title

    get_product_title.short_description = "Product Title" 


class VariantAdmin(CommonAdmin):
    search_fields = ("name", )
    list_display = get_list_display(Variant, ("variant2item", )) 
    list_display_links = ("name",)




admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(VariantItem, VariantItemAdmin)
admin.site.register(Variant, VariantAdmin)


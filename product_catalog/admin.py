from django.contrib import admin
from .models import (
    Product,
    Category,
    VariantItem,
    Variant,
    Tag
)

def get_list_display(model=None, exclude_fields=None):
    list_display = []
    for field in model._meta.get_fields(include_parents=False):
        if not field.name in exclude_fields:
            list_display.append(field.name)
    return list_display


class CommonAdmin(admin.ModelAdmin):
    readonly_fields = ["created_by"]
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.username == obj.created_by:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False # disable hard delete
        #if obj and not request.user.id == obj.created_by.id:
        #    return False
        #return True

# Register your models here.
class VariantItemInline(admin.TabularInline):
        model = VariantItem

class TagInline(admin.TabularInline):
        model = Tag

class ProductAdmin(CommonAdmin):
    readonly_fields = ["created_by"]
    inlines = (VariantItemInline,)
    list_display = get_list_display(Product, ("product2variantitem",))
    search_fields = ("name",)
    list_display_links = ("name",)



class CategoryAdmin(CommonAdmin):
    search_fields = ("name",)
    list_display_links = ("name",)
    list_display = get_list_display(Category, ("subcategories", "cat2product"))

    @admin.display(empty_value="Not applicable")
    def parent_name(self, obj):
        try:
            return obj.parent.name
        except:
            return obj.parent


class VariantItemAdmin(admin.ModelAdmin):
    search_fields = ("sku", "product__name")
    list_display_links = ("product__name",)
    list_display = ["id", "sku", "product__name", "get_variant_name", "options", "price", "default", "is_active", "date_created", "date_modified"]

    def get_variant_name(self, obj):
        return obj.product_variant.name

    get_variant_name.short_description = "Variant Name" 



class TagAdmin(CommonAdmin):
    readonly_fields = ["created_by"]
    filter_horizontal = ('product_variant',)
    search_fields = ("name",)
    list_display_links = ("name",)
    list_display = get_list_display(Category, ("subcategories", "cat2product", "img_upload", "parent", "level"))

class VariantAdmin(admin.ModelAdmin):
    pass



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(VariantItem, VariantItemAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Tag, TagAdmin)
from django.contrib import admin
from .models import (
    Product,
    Category,
    VariantItem,
    Tag
)

def get_list_display(model=None, exclude_fields=None):
    list_display = []
    for field in model._meta.get_fields(include_parents=False):
        if not field.name in exclude_fields:
            list_display.append(field.name)
    return list_display


class CommonAdmin(admin.ModelAdmin):
    #manually provide ur group?
    #readonly_fields = ["created_by"]
    def save_model(self, request, obj, form, change):
        #if not obj.created_by:
        #    obj.created_by = request.user.username
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        #if not belong to same group
        if obj and obj.vendor_name and not request.user.groups.filter(name=obj.vendor_name).exists():
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

class ProductAdmin(CommonAdmin):
    inlines = (VariantItemInline,)
    filter_horizontal = ('tag',)



class CategoryAdmin(CommonAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass




admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Tag, TagAdmin)
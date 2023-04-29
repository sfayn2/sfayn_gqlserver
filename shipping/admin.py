from django.contrib import admin
from .models import Zone, Method
from common import (
        CommonAdmin,
        get_list_display)

# Register your models here.
class ZoneAdmin(CommonAdmin):
    search_fields = ("name", "country", "region")
    list_display_links = ("name",)
    list_display = get_list_display(Zone, ("shipping_method",))
    list_display.append("get_shipping_methods")

    def get_shipping_methods(self, obj):
        return " | ".join([str(p) for p in obj.shipping_method.all()])

    get_shipping_methods.short_description = 'All Shipping Methods'


class MethodAdmin(CommonAdmin):
    search_fields = ("name", "desc",)
    filter_horizontal = ('classification', )
    list_display_links = ("name",)
    list_display = get_list_display(Method, ("classification", ))



admin.site.register(Zone, ZoneAdmin)
admin.site.register(Method, MethodAdmin)

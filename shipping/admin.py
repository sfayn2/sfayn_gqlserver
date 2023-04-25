from django.contrib import admin
from .models import Zone, Method
from common import (
        CommonAdmin,
        get_list_display)

# Register your models here.
class ZoneAdmin(CommonAdmin):
    search_fields = ("name", "country", "region")
    list_display_links = ("name",)
    list_display = get_list_display(Zone, ("zone2method",))


class MethodAdmin(CommonAdmin):
    search_fields = ("title", "desc",)
    filter_horizontal = ('zone', )
    list_display_links = ("title",)
    list_display = get_list_display(Method, ("zone",))
    list_display.append("get_zones")

    def get_zones(self, obj):
        return " | ".join([str(p) for p in obj.zone.all()])

    get_zones.short_description = 'Covered Zones' 



admin.site.register(Zone, ZoneAdmin)
admin.site.register(Method, MethodAdmin)

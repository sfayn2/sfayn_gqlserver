from django.contrib import admin
from .models import Zone, Method
from services import CommonAdmin

# Register your models here.
class ZoneAdmin(CommonAdmin):
    search_fields = ("name", "country", "region")
    list_display_links = ("name",)
    list_display = []
    for field in Zone._meta.get_fields():
        if not field.name in ("zone2method", ): #dont includ related 
            list_display.append(field.name)


class MethodAdmin(CommonAdmin):
    search_fields = ("title", "desc",)
    filter_horizontal = ('zone', 'tag')
    list_display_links = ("title",)
    list_display = []
    
    for field in Method._meta.get_fields():
        if not field.name in ("zone", "tag"):
            list_display.append(field.name)
    list_display.append("get_zones")
    list_display.append("get_tags")

    def get_zones(self, obj):
        return " | ".join([str(p) for p in obj.zone.all()])

    def get_tags(self, obj):
        return " | ".join([str(p) for p in obj.tag.all()])

    get_zones.short_description = 'Covered Zones' 
    get_tags.short_description = 'Covered Tags' 



admin.site.register(Zone, ZoneAdmin)
admin.site.register(Method, MethodAdmin)

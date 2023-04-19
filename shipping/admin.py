from django.contrib import admin
from .models import Zone, Method

# Register your models here.


class ZoneAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "region"]


class MethodAdmin(admin.ModelAdmin):
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

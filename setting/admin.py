from django.contrib import admin
from common import CommonAdmin
from .models import (
    Setting
)

# Register your models here.
class SettingAdmin(CommonAdmin):
    search_fields = ("name", "domain")
    list_display_links = ("name",)
    list_display = ("domain", "name", "weight_unit", "dimensions_unit", "product_approval", "country", "currency", "multi_vendor", "created_by", "date_created", "date_modified")


admin.site.register(Setting, SettingAdmin)

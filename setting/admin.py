from django.contrib import admin
from common import (
        CommonAdmin,
        get_list_display)
from .models import (
    Setting
)

# Register your models here.
class SettingAdmin(CommonAdmin):
    list_display_links = ("site",)
    list_display = get_list_display(Setting, ("",))


admin.site.register(Setting, SettingAdmin)

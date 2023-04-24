from django.contrib import admin
from common import (
        CommonAdmin,
        get_list_display)
from .models import (
    Vendor
)


# Register your models here.
class VendorAdmin(CommonAdmin):
    search_fields = ("name", "desc")
    list_display_links = ("name",)
    list_display = get_list_display(Vendor, ("vendor2discount",))
    readonly_fields = ["created_by", "status"]

admin.site.register(Vendor, VendorAdmin)

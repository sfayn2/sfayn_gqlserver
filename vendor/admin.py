from django.contrib import admin
from services import CommonAdmin
from .models import (
    Vendor
)


# Register your models here.
class VendorAdmin(CommonAdmin):
    search_fields = ("name", "desc")
    list_display_links = ("desc",)
    list_display = ("name", "desc", "logo", "status", "created_by", "date_created", "date_modified")

admin.site.register(Vendor, VendorAdmin)

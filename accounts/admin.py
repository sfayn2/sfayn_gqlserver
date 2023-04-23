from django.contrib import admin
from .models import Address, GroupProfile
from services import CommonAdmin

# Register your models here.
class AddressAdmin(CommonAdmin):
    #filter_horizontal = ('groups', )
    search_fields = ("country", )
    list_display = ("id", "address", "postal", "country", "region", "created_by")
    list_display_links = ("address",)


class GroupProfileAdmin(CommonAdmin):
    search_fields = ("name", )
    list_display = ("id", "name", "role", "created_by", "date_created", "date_modified")
    list_display_links = ("name",)


admin.site.register(Address, AddressAdmin)
admin.site.register(GroupProfile, GroupProfileAdmin)

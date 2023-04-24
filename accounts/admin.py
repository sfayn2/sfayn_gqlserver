from django.contrib import admin
from .models import Address, GroupProfile, Role
from services import CommonAdmin

# Register your models here.
class AddressAdmin(CommonAdmin):
    #filter_horizontal = ('groups', )
    search_fields = ("country", )
    list_display = ("id", "address", "postal", "country", "region", "created_by")
    list_display_links = ("address",)


class GroupProfileAdmin(CommonAdmin):
    filter_horizontal = ('role', )
    search_fields = ("name", )
    list_display = ("id", "name", "desc", "get_roles", "created_by", "date_created", "date_modified")
    list_display_links = ("name",)

    def get_roles(self, obj):
        if obj.role:
            return ", ".join([str(r) for r in obj.role.all()])
        else:
            return None


    get_roles.short_description = "Roles"


class RoleAdmin(CommonAdmin):
    search_fields = ("name", )
    list_display = ("id", "name", "created_by", "date_created", "date_modified")
    list_display_links = ("name",)


admin.site.register(Address, AddressAdmin)
admin.site.register(GroupProfile, GroupProfileAdmin)
admin.site.register(Role, RoleAdmin)

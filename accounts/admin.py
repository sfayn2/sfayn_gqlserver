from django.contrib import admin
from .models import Address

# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    #filter_horizontal = ('groups', )
    search_fields = ("country", )
    list_display = ("id", "address", "postal", "country", "region", "created_by")
    list_display_links = ("address",)


admin.site.register(Address, AddressAdmin)

from django.contrib import admin
from .models import (
    CustomerAddress
)

# Register your models here.
class CustomerAddressAdmin(admin.ModelAdmin):
    search_fields = ("fullname", "email")
    list_display = ("id", "address", )
    list_display_links = ("address",)

#admin.site.register(CustomerAddress, CustomerAddressAdmin)

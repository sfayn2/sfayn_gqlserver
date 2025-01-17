from django.contrib import admin
from customer_management.models import Customer, Address

# Register your models here.

class AddressInline(admin.TabularInline):
        model = Address

class CustomerAdmin(admin.ModelAdmin):
    inlines = (AddressInline,)
    list_display = ['user__email', 'user__first_name', 'user__last_name']

class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
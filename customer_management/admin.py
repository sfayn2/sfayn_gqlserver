from django.contrib import admin
from customer_management.models import Customer, Address

# Register your models here.

class AddressInline(admin.TabularInline):
        model = Address

class CustomerAdmin(admin.ModelAdmin):
    inlines = (AddressInline,)
    list_display = ['customer_id', 'user__first_name', 'user__last_name', 'user__email']

class AddressAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
from django.contrib import admin
from order_management.models import Order, OrderLine

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    pass

class OrderLineAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)

from django.contrib import admin
from order_management.models import (
    Order, 
    OrderLine,
    UserAuthorizationSnapshot,
)

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    pass

class OrderLineAdmin(admin.ModelAdmin):
    pass

class UserAuthorizationSnapshotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(UserAuthorizationSnapshot, UserAuthorizationSnapshotAdmin)

#just a snapshots
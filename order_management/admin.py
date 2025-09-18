from django.contrib import admin
from order_management.models import (
    Order, 
    LineItem,
    UserAuthorizationSnapshot,
)

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    pass

class LineItemAdmin(admin.ModelAdmin):
    pass

class UserAuthorizationSnapshotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(UserAuthorizationSnapshot, UserAuthorizationSnapshotAdmin)

#just a snapshots
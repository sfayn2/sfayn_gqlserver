from django.contrib import admin
from order_management.models import (
    Order, 
    OrderLine,
    UserAuthorizationSnapshot,
    VendorDetailsSnapshot,
    VendorCouponSnapshot,
    VendorOfferSnapshot,
    VendorShippingOptionSnapshot,
    VendorProductSnapshot,
    CustomerDetailsSnapshot,
    CustomerAddressSnapshot,
)

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    pass

class OrderLineAdmin(admin.ModelAdmin):
    pass

class VendorDetailsSnapshotAdmin(admin.ModelAdmin):
    pass

class VendorCouponSnapshotAdmin(admin.ModelAdmin):
    pass

class VendorOfferSnapshotAdmin(admin.ModelAdmin):
    pass

class VendorShippingOptionSnapshotAdmin(admin.ModelAdmin):
    pass

class VendorProductSnapshotAdmin(admin.ModelAdmin):
    pass

class CustomerDetailsSnapshotAdmin(admin.ModelAdmin):
    pass

class CustomerAddressSnapshotAdmin(admin.ModelAdmin):
    pass

class UserAuthorizationSnapshotAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(UserAuthorizationSnapshot, UserAuthorizationSnapshotAdmin)

#just a snapshots
admin.site.register(VendorDetailsSnapshot, VendorDetailsSnapshotAdmin)
admin.site.register(VendorCouponSnapshot, VendorCouponSnapshotAdmin)
admin.site.register(VendorOfferSnapshot, VendorOfferSnapshotAdmin)
admin.site.register(VendorShippingOptionSnapshot, VendorShippingOptionSnapshotAdmin)
admin.site.register(VendorProductSnapshot, VendorProductSnapshotAdmin)
admin.site.register(CustomerDetailsSnapshot, CustomerDetailsSnapshotAdmin)
admin.site.register(CustomerAddressSnapshot, CustomerAddressSnapshotAdmin)

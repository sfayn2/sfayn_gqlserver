from django.contrib import admin
from vendor_management.models import Offer, ShippingOption, Vendor, Coupon

# Register your models here.

class OfferInline(admin.TabularInline):
        model = Offer

class ShippingOptionInline(admin.TabularInline):
        model = ShippingOption

class VendorAdmin(admin.ModelAdmin):
    pass

    #too many fields? 
    #inlines = (ShippingOptionInline, OfferInline)

class ShippingOptionAdmin(admin.ModelAdmin):
    pass

class OfferAdmin(admin.ModelAdmin):
    filter_horizontal = ('coupon',)

class CouponAdmin(admin.ModelAdmin):
      pass


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(ShippingOption, ShippingOptionAdmin)
admin.site.register(Coupon, CouponAdmin)
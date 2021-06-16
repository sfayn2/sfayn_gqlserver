from django.contrib import admin
from .models import (
    PaymentMethod
)

# Register your models here.
class PaymentMethodAdmin(admin.ModelAdmin):
    search_fields = ("method",)
    list_display = ("id", "method", )
    list_display_links = ("method",)

admin.site.register(PaymentMethod, PaymentMethodAdmin)


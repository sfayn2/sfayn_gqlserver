from django.contrib import admin
from common import (
        CommonAdmin,
        get_list_display
        )
from .models import (
    PaymentMethod
)

# Register your models here.
class PaymentMethodAdmin(CommonAdmin):
    search_fields = ("method",)
    list_display_links = ("method",)
    list_display = get_list_display(PaymentMethod, ("payment2order",))

admin.site.register(PaymentMethod, PaymentMethodAdmin)


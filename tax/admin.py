from django.contrib import admin
from .models import Tax
from common import (
        CommonAdmin,
        get_list_display)

# Register your models here.
class TaxAdmin(CommonAdmin):
    search_fields = ("name", "country")
    list_display_links = ("name",)
    list_display = get_list_display(Tax, ("tax2order",)) 



admin.site.register(Tax, TaxAdmin)

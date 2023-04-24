from django.contrib import admin
from .models import Tax
from common import CommonAdmin

# Register your models here.
class TaxAdmin(CommonAdmin):
    search_fields = ("name", "country")
    list_display_links = ("name",)
    list_display = ("name", "country", "rate", "created_by", "date_created", "date_modified")



admin.site.register(Tax, TaxAdmin)

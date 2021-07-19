from django.contrib import admin
from .models import (
    PromotionalBanner
)

# Register your models here.
class PromotionalBannerAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "img_upload", "img_url")

admin.site.register(PromotionalBanner, PromotionalBannerAdmin)

from django.contrib import admin
from django.conf import settings
from common import (
        CommonAdmin,
        get_list_display)
from .models import (
    Tag,
)

# Register your models here.
class TagAdmin(CommonAdmin):
    search_fields = ("name",)
    filter_horizontal = ("product_variant",)
    list_display_links = ("name",)
    list_display = get_list_display(Tag, ("product_variant", "tag2method", "tag2discount"))

admin.site.register(Tag, TagAdmin)

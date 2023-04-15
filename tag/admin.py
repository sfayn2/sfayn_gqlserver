from django.contrib import admin
from django.conf import settings
from .models import (
    Tag,
    TagItem,
)

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)


class TagItemAdmin(admin.ModelAdmin):
    search_fields = ("tag",)
    list_display = ("tag", "product_variant")

admin.site.register(Tag, TagAdmin)
admin.site.register(TagItem, TagItemAdmin)

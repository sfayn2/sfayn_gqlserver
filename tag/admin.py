from django.contrib import admin
from django.conf import settings
from .models import (
    Tag,
    TagItem,
)

class TagItemInline(admin.TabularInline):
    model = TagItem

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)

    inlines = [
        TagItemInline,
    ]



admin.site.register(Tag, TagAdmin)

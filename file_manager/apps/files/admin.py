from django.contrib import admin

from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "width", "height", "created_at", "updated_at")
    search_fields = ("title",)
    ordering = ("-updated_at",)
    list_filter = ("updated_at",)

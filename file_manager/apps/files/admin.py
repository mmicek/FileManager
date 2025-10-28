from django.contrib import admin

from .api.services.image_service import ImageService
from .models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "width", "height", "created_at", "updated_at")
    search_fields = ("title",)
    ordering = ("-updated_at",)
    list_filter = ("updated_at",)

    def save_model(self, request, obj, form, change):
        width = form.cleaned_data.get("width")
        height = form.cleaned_data.get("height")
        image_service = ImageService(obj.image)

        if width and height:
            obj.image = image_service.resize_image(obj.width, obj.height)
        else:
            width, height = image_service.get_image_size()

        obj.width, obj.height = width, height
        super().save_model(request, obj, form, change)

from apps.common.enums import MediaType
from apps.common.validators import MediaTypeValidator
from apps.files.models import Image
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        validators=[MediaTypeValidator([MediaType.JPEG, MediaType.PNG, MediaType.JPG])], write_only=True
    )
    url = serializers.SerializerMethodField(read_only=True)

    width = serializers.IntegerField(required=False)
    height = serializers.IntegerField(required=False)

    class Meta:
        model = Image
        fields = ["id", "image", "url", "title", "width", "height", "updated_at", "created_at"]
        read_only_fields = ["id", "updated_at", "url"]

    def get_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

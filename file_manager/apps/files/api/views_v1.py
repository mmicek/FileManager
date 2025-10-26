from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from ...common.paginations import CustomPageNumberPagination
from ..models import Image
from .serializers import ImageSerializer
from .services.image_service import ImageService


class ImageViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Image.objects.all().order_by("-updated_at")
    serializer_class = ImageSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]  # Set search parameter name e.g ?title=...

    def perform_create(self, serializer) -> Response:
        """
        Handle creation of a new Image instance.
        If width and height are provided, the image is resized.
        Otherwise, the original image dimensions are used.
        """

        image_file = serializer.validated_data["image"]
        width = serializer.validated_data.get("width")
        height = serializer.validated_data.get("height")

        image_service = ImageService(image_file)
        if width and height:
            image_file = image_service.resize_image(width, height)
        else:
            width, height = image_service.get_image_size()

        serializer.save(image=image_file, width=width, height=height)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

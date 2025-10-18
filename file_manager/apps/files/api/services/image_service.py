from io import BytesIO

from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image as PILImage


class ImageService:
    """
    Service class for handling image operations such as resizing
    and getting image dimensions.

    Attributes:
        file (Any): File-like object representing the image.
    """

    def __init__(self, file: File):
        self.file: File = file

    def resize_image(self, width: int, height: int) -> ContentFile:
        """
        Resize image to given width and height.
        Returns ContentFile ready to save in ImageField.
        """
        img = PILImage.open(self.file)
        img = img.resize((width, height))

        img_io = BytesIO()
        img_format = img.format or "PNG"
        img.save(img_io, format=img_format)
        return ContentFile(img_io.getvalue(), name=getattr(self.file, "name", "image.png"))

    def get_image_size(self) -> tuple[int, int]:
        """
        Return width and height of the image.
        """
        img = PILImage.open(self.file)
        return img.width, img.height

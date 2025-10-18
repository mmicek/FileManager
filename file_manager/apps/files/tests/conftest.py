import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage


@pytest.fixture
def valid_image() -> SimpleUploadedFile:
    """
    Fixture that returns a valid PNG image file suitable for upload.
    """
    file = io.BytesIO()
    img = PILImage.new("RGB", (100, 100), color="red")
    img.save(file, format="PNG")
    file.seek(0)
    return SimpleUploadedFile(name="test.png", content=file.getvalue(), content_type="image/png")


@pytest.fixture
def invalid_image() -> SimpleUploadedFile:
    """
    Fixture that returns a invalid PNG image file suitable for upload.
    """
    file = io.BytesIO()
    img = PILImage.new("RGB", (100, 100), color="red")
    img.save(file, format="GIF")
    file.seek(0)
    return SimpleUploadedFile(name="invalid_format.gif", content=file.getvalue(), content_type="text/plain")

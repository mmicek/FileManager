import pytest
from apps.files.models import Image
from django.urls import reverse
from rest_framework import status


class TestImageViewSet:

    @pytest.mark.django_db
    def test_upload_image(self, auth_client_token, valid_image):
        url = reverse("files-api-v1:image-list")
        data = {
            "title": "Test Image",
            "width": 50,
            "height": 50,
            "image": valid_image,
        }

        response = auth_client_token.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Test Image"
        assert response.data["width"] == 50
        assert response.data["height"] == 50
        assert "url" in response.data
        assert Image.objects.count() == 1

    @pytest.mark.django_db
    def test_upload_image_already_exists(self, auth_client_token, valid_image):
        # TODO Use factory here
        Image.objects.create(title="Test Image", image=valid_image, width=100, height=100)
        url = reverse("files-api-v1:image-list")
        data = {
            "title": "Test Image",
            "width": 50,
            "height": 50,
            "image": valid_image,
        }

        response = auth_client_token.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Image.objects.count() == 1

    @pytest.mark.django_db
    def test_upload_image_no_resize(self, auth_client_token, valid_image):
        url = reverse("files-api-v1:image-list")
        data = {
            "title": "Original Size",
            "image": valid_image,
        }

        response = auth_client_token.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["width"] > 0
        assert response.data["height"] > 0

    @pytest.mark.django_db
    def test_list_images(self, auth_client_token, valid_image):
        # TODO Use factory here
        Image.objects.create(title="Cat", image=valid_image, width=100, height=100)
        Image.objects.create(title="Dog", image=valid_image, width=100, height=100)

        url = reverse("files-api-v1:image-list")
        response = auth_client_token.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2

        response = auth_client_token.get(url + "?search=ca")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert "Cat" in response.data["results"][0]["title"]
        assert "url" in response.data["results"][0]

    @pytest.mark.django_db
    def test_get_single_image(self, auth_client_token, valid_image):
        image = Image.objects.create(title="Sunset", image=valid_image, width=100, height=100)
        url = reverse("files-api-v1:image-detail", kwargs={"pk": image.id})
        response = auth_client_token.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == image.id
        assert response.data["title"] == "Sunset"
        assert "url" in response.data
        assert "http://" in response.data["url"]  # noqa

    @pytest.mark.django_db
    def test_invalid_media_type(self, auth_client_token, invalid_image):
        url = reverse("files-api-v1:image-list")
        data = {"title": "Bad File", "image": invalid_image, "overwrite": "true"}

        response = auth_client_token.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Please upload a valid media file" in str(response.data)

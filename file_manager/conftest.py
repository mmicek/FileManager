import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="test", password="test")


@pytest.fixture
def token(user):
    return Token.objects.create(user=user)


@pytest.fixture
def auth_client_token(client, token):
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client

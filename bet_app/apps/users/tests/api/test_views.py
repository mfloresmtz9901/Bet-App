from datetime import datetime, timezone
from http import HTTPStatus

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from jose import jwt

from bet_app.apps.users.api.auth import create_access_token
from bet_app.apps.users.models import User
from bet_app.apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return UserFactory.create()


def test_list_users_as_anonymous_user(client: Client):
    response = client.get(reverse("api:list_users"))

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_list_users_as_authenticated_user(client: Client, user: User):
    client.force_login(user)
    # Another user, excluded from the response
    UserFactory.create()

    response = client.get(reverse("api:list_users"))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            "email": user.email,
            "name": user.name,
            "url": f"/api/users/{user.username}/",
            "username": user.username,
        },
    ]


def test_retrieve_current_user(client: Client, user: User):
    client.force_login(user)

    response = client.get(
        reverse("api:retrieve_current_user"),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": user.email,
        "name": user.name,
        "url": f"/api/users/{user.username}/",
        "username": user.username,
    }


def test_retrieve_user(client: Client, user: User):
    client.force_login(user)

    response = client.get(
        reverse("api:retrieve_user", kwargs={"username": user.username}),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": user.email,
        "name": user.name,
        "url": f"/api/users/{user.username}/",
        "username": user.username,
    }


def test_retrieve_another_user(client: Client, user: User):
    client.force_login(user)
    user_2 = UserFactory.create()

    response = client.get(
        reverse("api:retrieve_user", kwargs={"username": user_2.username}),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Not Found"}


def test_update_current_user(client: Client):
    user = UserFactory.create(name="Old")
    client.force_login(user)

    response = client.patch(
        reverse("api:update_current_user"),
        data='{"name": "New Name", "username": "old"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK, response.json()
    assert response.json() == {
        "email": user.email,
        "name": "New Name",
        "username": "old",
        "url": "/api/users/old/",
    }


def test_update_user(client: Client):
    user = UserFactory.create(name="Old", username="old")
    client.force_login(user)

    response = client.patch(
        reverse("api:update_user", kwargs={"username": "old"}),
        data='{"name": "New Name", "username": "old"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK, response.json()
    assert response.json() == {
        "email": user.email,
        "name": "New Name",
        "url": "/api/users/old/",
        "username": "old",
    }


def test_login_success(client: Client):
    user = UserFactory.create(password="testpass123!")

    response = client.post(
        reverse("api:login"),
        data=f'{{"email": "{user.email}", "password": "testpass123!"}}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.OK
    assert settings.JWT_AUTH_COOKIE_NAME in response.cookies
    assert response.json() == {"message": "Login successful"}


def test_login_invalid_password(client: Client):
    user = UserFactory.create(password="testpass123!")

    response = client.post(
        reverse("api:login"),
        data=f'{{"email": "{user.email}", "password": "wrongpass"}}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_unknown_email(client: Client):
    response = client.post(
        reverse("api:login"),
        data='{"email": "nobody@example.com", "password": "irrelevant"}',
        content_type="application/json",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_retrieve_current_user_with_jwt(client: Client):
    user = UserFactory.create()
    token = create_access_token(user.id)
    client.cookies[settings.JWT_AUTH_COOKIE_NAME] = token

    response = client.get(reverse("api:retrieve_current_user"))

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "email": user.email,
        "name": user.name,
        "url": f"/api/users/{user.username}/",
        "username": user.username,
    }


def test_retrieve_current_user_with_expired_jwt(client: Client):
    user = UserFactory.create()
    expired_payload = {"user_id": user.id, "exp": int(
        datetime(2020, 1, 1, tzinfo=timezone.utc).timestamp())}
    token = jwt.encode(expired_payload, settings.SECRET_KEY, algorithm="HS256")
    client.cookies[settings.JWT_AUTH_COOKIE_NAME] = token

    response = client.get(reverse("api:retrieve_current_user"))

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_retrieve_current_user_with_invalid_jwt(client: Client):
    client.cookies[settings.JWT_AUTH_COOKIE_NAME] = "not.a.valid.token"

    response = client.get(reverse("api:retrieve_current_user"))

    assert response.status_code == HTTPStatus.UNAUTHORIZED

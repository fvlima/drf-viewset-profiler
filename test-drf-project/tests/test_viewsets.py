import pytest
import status
from django.test import override_settings
from django.urls import reverse
from model_mommy import mommy

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "url,method,data,expected_code",
    (
        ("/api/test-viewset/", "get", {}, status.HTTP_200_OK),
        ("/api/test-viewset/", "post", {"name": "John Doe"}, status.HTTP_201_CREATED),
        ("/api/test-viewset/1/", "put", {"name": "John"}, status.HTTP_200_OK),
        ("/api/test-viewset/1/", "patch", {"name": "Doe"}, status.HTTP_200_OK),
        ("/api/test-viewset/1/", "delete", {}, status.HTTP_204_NO_CONTENT),
    ),
)
def test_line_profiler_viewset(api_client, url, method, data, expected_code, mock_output_writer):
    method = getattr(api_client, method)
    response = method(url, data=data) if data else method(url)

    assert response.status_code == expected_code
    assert mock_output_writer.called is True


def test_line_profiler_model_viewset_get(api_client, mock_output_writer):
    mommy.make("testapp.TestModel")
    url = reverse("testapp:test-model-viewset-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert mock_output_writer.called is True


def test_line_profiler_model_viewset_post(api_client, mock_output_writer):
    url = reverse("testapp:test-model-viewset-list")
    response = api_client.post(url, data={"name": "John Doe"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"name": "John Doe"}
    assert mock_output_writer.called is True


@pytest.mark.parametrize("method", ("put", "patch"))
def test_line_profiler_model_viewset_update(api_client, method, mock_output_writer):
    model = mommy.make("testapp.TestModel")
    url = reverse("testapp:test-model-viewset-detail", args=[model.pk])
    method = getattr(api_client, method)
    response = method(url, data={"name": "John Doe"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "John Doe"}
    assert mock_output_writer.called is True


def test_line_profiler_model_viewset_delete(api_client, mock_output_writer):
    model = mommy.make("testapp.TestModel")
    url = reverse("testapp:test-model-viewset-detail", args=[model.pk])
    response = api_client.delete(url, data={"name": "John Doe"})

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert mock_output_writer.called is True


@override_settings(
    MIDDLEWARE=[
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]
)
def test_line_profiler_viewset_without_middleware_config(api_client, mock_output_writer):
    url = reverse("testapp:test-model-viewset-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert mock_output_writer.called is False

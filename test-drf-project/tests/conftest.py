from unittest import mock

import pytest
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.test import APIClient

from drf_viewset_profiler.middleware import LineProfilerViewSetMiddleware


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def mock_http_request():
    http_request = HttpRequest()
    http_request.method = "GET"
    return http_request


@pytest.fixture
def mock_http_response(mock_http_request):
    response = Response()
    mock_http_request.line_profiler = mock.Mock()
    mock_http_request.parser_context = {"view": mock.Mock()}
    response.renderer_context = {"request": mock_http_request}
    return response


@pytest.fixture
def mock_output_writer(monkeypatch):
    mock_output_writer_ = mock.Mock()
    monkeypatch.setattr("drf_viewset_profiler.middleware.output_writer.stream", mock_output_writer_)
    return mock_output_writer_


@pytest.fixture
def mock_line_profiler_viewset_middleware():
    return LineProfilerViewSetMiddleware()

from unittest import mock

import pytest
from line_profiler import LineProfiler
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from drf_viewset_profiler.decorators import line_profiler_viewset


class TestSerializer:
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class BaseTestView:
    def create(self, request):
        return Response()


def test_decorator_verifying_line_profile_viewset(mock_http_request):
    @line_profiler_viewset
    class TestViewSet(BaseTestView, viewsets.ViewSet):
        pass

    viewset = TestViewSet.as_view({"post": "create"})(mock_http_request)
    functions = viewset.renderer_context["request"].line_profiler.functions

    assert TestViewSet.create in functions


def test_decorator_verifying_line_profile_modelviewset_with_serializer_class(mock_http_request):
    @line_profiler_viewset
    class TestModelViewSet(BaseTestView, viewsets.ModelViewSet):
        serializer_class = TestSerializer

    viewset = TestModelViewSet.as_view({"post": "create"})(mock_http_request)
    functions = viewset.renderer_context["request"].line_profiler.functions

    assert TestModelViewSet.create in functions
    assert TestSerializer.create in functions
    assert TestSerializer.update in functions


def test_decorator_verifying_line_profile_modelviewset_with_get_serializer_class(mock_http_request):
    @line_profiler_viewset
    class TestModelViewSet(BaseTestView, viewsets.ModelViewSet):
        def get_serializer_class(self):
            return TestSerializer

    viewset = TestModelViewSet.as_view({"post": "create"})(mock_http_request)
    functions = viewset.renderer_context["request"].line_profiler.functions

    assert TestModelViewSet.create in functions
    assert TestSerializer.create in functions
    assert TestSerializer.update in functions


def test_decorator_verifying_line_profile_modelviewset_without_get_serializer_class(mock_http_request):
    @line_profiler_viewset
    class TestModelViewSet(BaseTestView, viewsets.ModelViewSet):
        pass

    with pytest.raises(AssertionError):
        TestModelViewSet.as_view({"post": "create"})(mock_http_request)


@mock.patch("drf_viewset_profiler.decorators.enable_serializer_profiler", False)
def test_decorator_verifying_line_profile_modelviewset_with_profiling_serializer_false(mock_http_request):
    @line_profiler_viewset
    class TestModelViewSet(BaseTestView, viewsets.ModelViewSet):
        def get_serializer_class(self):
            return TestSerializer

    viewset = TestModelViewSet.as_view({"post": "create"})(mock_http_request)
    functions = viewset.renderer_context["request"].line_profiler.functions

    assert TestModelViewSet.create in functions
    assert TestSerializer.create not in functions
    assert TestSerializer.update not in functions


@mock.patch("drf_viewset_profiler.decorators.enable_serializer_profiler", False)
@pytest.mark.parametrize("viewset_type", (viewsets.ViewSet, viewsets.ModelViewSet))
def test_decorator_verifying_request_line_profiler_instance(viewset_type, mock_http_request):
    @line_profiler_viewset
    class TestViewSet(viewset_type):
        pass

    viewset = TestViewSet(action_map={})
    request = viewset.initialize_request(mock_http_request)

    assert isinstance(request, Request)
    assert hasattr(request, "line_profiler")
    assert isinstance(request.line_profiler, LineProfiler)


def test_decorator_verifying_name():
    @line_profiler_viewset
    class TestViewSet:
        pass

    assert TestViewSet.__name__ == "TestViewSet"

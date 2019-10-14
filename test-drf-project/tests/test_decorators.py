import pytest
from line_profiler import LineProfiler
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from drf_viewset_profiler.decorators import line_profiler_viewset


class BaseTestView:
    actions = {
        "get": "list",  # noqa
        "post": "create",
        "get": "retrieve",  # noqa
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }

    def __str__(self):
        pass

    def _some_private_method(self):
        pass

    def create(self, request):
        return Response()

    def list(self, request):
        return Response()

    def retrieve(self, request, pk=None):
        return Response()

    def update(self, request, pk=None):
        return Response()

    def partial_update(self, request, pk=None):
        return Response()

    def destroy(self, request, pk=None):
        return Response()


@pytest.mark.parametrize("viewset_type", (viewsets.ViewSet, viewsets.ModelViewSet))
def test_decorator_verifying_line_profile_functions(viewset_type, mock_http_request):
    @line_profiler_viewset
    class TestViewSet(BaseTestView, viewset_type):
        pass

    actions = BaseTestView.actions
    viewset = TestViewSet.as_view(actions)(mock_http_request)
    functions = viewset.renderer_context["request"].line_profiler.functions

    assert TestViewSet.actions not in functions
    assert TestViewSet.__str__ in functions
    assert TestViewSet._some_private_method in functions
    assert TestViewSet.create in functions
    assert TestViewSet.list in functions
    assert TestViewSet.retrieve in functions
    assert TestViewSet.update in functions
    assert TestViewSet.partial_update in functions
    assert TestViewSet.destroy in functions


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

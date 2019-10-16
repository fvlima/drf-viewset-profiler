from .utils import create_line_profile, get_value_from_config

enable_serializer_profiler = get_value_from_config("ENABLE_SERIALIZER_PROFILER", True)


def line_profiler_viewset(viewset):
    """
    Decorator to profile all methods from a viewset line by line.
    For all methods that were called during a request, an output
    will be generated showing the number of hits, time, lines and the
    content of each line of a method that was executed.

    Example of usage:

    - Decorate the viewset that will be profiled

    @line_profiler_viewset
    class SomeViewSet(ViewSet):
        queryset = Model.objects.all()

    -  Set the middleware config in settings.py

    MIDDLEWARE = [
        ...
        "drf_viewset_profiler.middleware.LineProfilerViewSetMiddleware"
    ]
    """

    class LineProfilerViewSet(viewset):
        def initialize_request(self, request, *args, **kwargs):
            request = super().initialize_request(request, *args, **kwargs)
            args = [viewset]

            if enable_serializer_profiler and hasattr(viewset, "get_serializer_class"):
                args.append(viewset.get_serializer_class(self))

            request.line_profiler = create_line_profile(*args)
            return request

    LineProfilerViewSet.__name__ = viewset.__name__
    return LineProfilerViewSet

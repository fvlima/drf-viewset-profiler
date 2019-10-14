from django.utils.deprecation import MiddlewareMixin

from .output import output_writer


class LineProfilerViewSetMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        try:
            request = response.renderer_context["request"]

            if not hasattr(request, "line_profiler"):
                return response

            view = request.parser_context["view"]
            view_name = view.__class__.__name__

            with output_writer(view_name) as stream:
                request.line_profiler.print_stats(stream=stream, stripzeros=True)
        except AttributeError:
            pass

        return response

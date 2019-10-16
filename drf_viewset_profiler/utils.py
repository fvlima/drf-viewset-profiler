import inspect

from django.conf import settings
from line_profiler import LineProfiler

drf_viewset_config = getattr(settings, "DRF_VIEWSET_PROFILER", {})


def create_line_profile(*args):
    line_profiler = LineProfiler()
    line_profiler.enable_by_count()

    for klass in args:
        for attr in dir(klass):
            func = getattr(klass, attr)
            condition = (not inspect.isfunction(func), not inspect.ismethod(func))
            if all(condition):
                continue
            line_profiler.add_function(func)

    return line_profiler


def get_value_from_config(config, default):
    return drf_viewset_config.get(config, default)

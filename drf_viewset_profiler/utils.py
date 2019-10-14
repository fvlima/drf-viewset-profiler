import inspect

from line_profiler import LineProfiler


def create_line_profile(klass):
    line_profiler = LineProfiler()
    line_profiler.enable_by_count()

    for attr in dir(klass):
        func = getattr(klass, attr)
        condition = (not inspect.isfunction(func), not inspect.ismethod(func))
        if all(condition):
            continue
        line_profiler.add_function(func)

    return line_profiler

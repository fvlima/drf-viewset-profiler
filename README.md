[![PyPI latest](https://img.shields.io/pypi/v/drf-viewset-profiler.svg)](https://pypi.python.org/pypi/drf-viewset-profiler)
[![Build Status](https://travis-ci.org/fvlima/drf-viewset-profiler.svg?branch=master)](https://travis-ci.org/fvlima/drf-viewset-profiler)

# drf-viewset-profiler

Decorator to profile all methods from a viewset (and its serializer) line by line. For all methods that were called during a request, an output
will be generated showing the number of hits, time (in seconds), lines and the content of each line of a method that was executed

## Installation

`pip install drf-viewset-profiler`

Note: due to a problem with `line_profiler` installation, it's necessary to follow these instructions [1] to install, or just do: 

- `pip install Cython`
- `pip install git+https://github.com/rkern/line_profiler#egg=line_profiler`
- `pip install drf-viewset-profiler --no-deps`

1 - https://github.com/rkern/line_profiler#installation

## Usage

Decorate the viewset that will be profiled

```python
from drf_viewset_profiler import line_profiler_viewset

@line_profiler_viewset
class SomeViewSet(ViewSet):
    queryset = Model.objects.all()
```

Set the middleware config in settings.py

```python
MIDDLEWARE = [
    ...
    "drf_viewset_profiler.middleware.LineProfilerViewSetMiddleware"
]
```

Make requests in this viewset to profile and measure the time in seconds wasted

## Configuration

```python
DRF_VIEWSET_PROFILER = {
    "DEFAULT_OUTPUT_GENERATION_TYPE": "drf_viewset_profiler.output.FileOutput",
    "DEFAULT_OUTPUT_LOCATION": "",
    "ENABLE_SERIALIZER_PROFILER": True
}
```

#### DEFAULT_OUTPUT_GENERATION_TYPE
- drf_viewset_profiler.output.FileOutput: generates the output in a txt file with the name of the profiled viewset
- drf_viewset_profiler.output.StdOutput: generates the output in the console (default)

It's possible to customize by extending the BaseOuput class

#### DEFAULT_OUTPUT_LOCATION
- the location to generate the output file with the name of the view that will profiled (default is empty)

#### ENABLE_SERIALIZER_PROFILER
- profile the methods from the serializer vinculated with the viewset (default is True)

#### Output example

```
Total time: 1.7e-05 s
File: /.pyenv/versions/3.7.4/envs/drf-viewset-profiler/lib/python3.7/site-packages/django/views/generic/base.py
Function: _allowed_methods at line 113

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
113                                               def _allowed_methods(self):
114         1         17.0     17.0    100.0          return [m.upper() for m in self.http_method_names if hasattr(self, m)]

Total time: 0.000158 s
File: /.pyenv/versions/3.7.4/envs/drf-viewset-profiler/lib/python3.7/site-packages/rest_framework/generics.py
Function: get_serializer at line 103

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
103                                               def get_serializer(self, *args, **kwargs):
104                                                   """
105                                                   Return the serializer instance that should be used for validating and
106                                                   deserializing input, and for serializing output.
107                                                   """
108         1         15.0     15.0      9.5          serializer_class = self.get_serializer_class()
109         1         12.0     12.0      7.6          kwargs['context'] = self.get_serializer_context()
110         1        131.0    131.0     82.9          return serializer_class(*args, **kwargs)

Total time: 4e-06 s
File: /.pyenv/versions/3.7.4/envs/drf-viewset-profiler/lib/python3.7/site-packages/rest_framework/generics.py
Function: get_serializer_class at line 112

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
112                                               def get_serializer_class(self):
113                                                   """
114                                                   Return the class to use for the serializer.
115                                                   Defaults to using `self.serializer_class`.
116  
117                                                   You may want to override this if you need to provide different
118                                                   serializations depending on the incoming request.
119  
120                                                   (Eg. admins get full serialization, others get basic serialization)
121                                                   """
122         1          3.0      3.0     75.0          assert self.serializer_class is not None, (
123                                                       "'%s' should either include a `serializer_class` attribute, "
124                                                       "or override the `get_serializer_class()` method."
125                                                       % self.__class__.__name__
126                                                   )
127  
128         1          1.0      1.0     25.0          return self.serializer_class  

...

Total time: 1.5491 s
File: /drf-viewset-profiler/test-drf-project/testapp/views.py
Function: create at line 52

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    52                                               def create(self, request):
    53         1          4.0      4.0      0.0          import time
    54         1    1505235.0 1505235.0     97.2          time.sleep(1.5)
    55         1      43866.0  43866.0      2.8          return super().create(request)  
```  

## Contribute

- Clone this repository
- Install poetry (pip install poetry)
- run `poetry install`
- run `pre-commit install`
- Create your branch, make changes and open the pull request

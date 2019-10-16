0.2.0
~~~~~

* Improve BaseOutput to handle file location bevavior
* Add utils get_value_from_config function to retrieve drf viewset configs
* Add readme to pyprojec.toml to generate the long description in setup.py
* Add configuration `ENABLE_SERIALIZER_PROFILER`. In cases when this config is True and the viewset
has the `get_serializer_class` method, the decorator line_profiler_viewset will automatically profile
the methods and functions from the serializer vinculated with the viewset
* Add support to python 3.8

0.1.0
~~~~~

* Initial release
* Add line_profiler_viewset decorator to profile all methods from a viewset line by line

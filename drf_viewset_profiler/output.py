import sys

from django.conf import settings
from django.utils.module_loading import import_string

drf_viewset_config = getattr(settings, "DRF_VIEWSET_PROFILER", {})
output_generation_type = drf_viewset_config.get(
    "DEFAULT_OUTPUT_GENERATION_TYPE", "drf_viewset_profiler.output.StdOutput"
)
output_default_location = drf_viewset_config.get("DEFAULT_OUTPUT_LOCATION", "")


class BaseOutput:
    stream = None

    def __init__(self, file_name=None):
        self.file_name = file_name.strip().lower() if file_name else ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stream.close()

    def write(self, data):
        self.stream.write(data)

    def writelines(self, data):
        self.stream.writelines(data)

    def get_file_name(self):
        raise NotImplementedError()


class StdOutput(BaseOutput):
    stream = sys.stdout

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stream.flush()


class FileOutput(BaseOutput):
    def __init__(self, file_name):
        super().__init__(file_name)
        self.stream = open(self.get_file_name(), "w")

    def get_file_name(self):
        return output_default_location + self.file_name


output_writer = import_string(output_generation_type)

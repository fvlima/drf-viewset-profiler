import sys

from django.utils.module_loading import import_string

from .utils import get_value_from_config


class BaseOutput:
    stream = None
    output_location = get_value_from_config("DEFAULT_OUTPUT_LOCATION", "")

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

    def get_file_location(self):
        output_location = self.output_location
        if output_location is None:
            output_location = ""
        if output_location and not output_location.endswith("/"):
            output_location = output_location + "/"
        return output_location + self.file_name


class StdOutput(BaseOutput):
    stream = sys.stdout

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stream.flush()


class FileOutput(BaseOutput):
    def __init__(self, file_name):
        super().__init__(file_name)
        self.stream = open(self.get_file_location(), "w")


_output_generation_type = get_value_from_config(
    "DEFAULT_OUTPUT_GENERATION_TYPE", "drf_viewset_profiler.output.StdOutput"
)
output_writer = import_string(_output_generation_type)

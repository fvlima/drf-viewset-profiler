from unittest import mock

import pytest

from drf_viewset_profiler.output import BaseOutput, FileOutput, StdOutput


@pytest.fixture
def base_output():
    base_output = BaseOutput()
    base_output.stream = mock.Mock()
    return base_output


def test_base_output_without_name(base_output):
    assert base_output.file_name == ""


@pytest.mark.parametrize("filename", ("Name", "NAME", "nAme", "name", "name ", " name", " name "))
def test_base_output_with_name(base_output, filename):
    assert BaseOutput(filename).file_name == "name"


def test_base_output_get_file_name(base_output):
    with pytest.raises(NotImplementedError):
        assert base_output.get_file_name()


def test_base_output_without_defined_stream():
    assert BaseOutput().stream is None


def test_base_output_context_manager(base_output):
    with base_output as stream:
        assert isinstance(stream, BaseOutput)

    assert base_output.stream.close.called is True


@pytest.mark.parametrize("data", ("foo", ("foo", "bar")))
def test_base_output_write(base_output, data):
    with base_output:
        for item in data:
            base_output.write(item)

    base_output.stream.write.assert_has_calls([mock.call(item) for item in data])


@pytest.mark.parametrize("data", ("foo", ("foo", "bar")))
def test_base_output_writelines(base_output, data):
    with base_output:
        base_output.writelines(data)

    base_output.stream.writelines.assert_has_calls([mock.call(data)])


def test_std_output():
    std_output = StdOutput()
    std_output.stream = mock.Mock()

    with std_output as stream:
        stream.write("foo")

    assert std_output.stream.flush.called is True


@mock.patch("builtins.open")
def test_file_output(mock_open):
    file_output = FileOutput("name")

    with file_output as stream:
        stream.write("bar")

    assert mock_open.call_args_list[0] == mock.call("name", "w")
    assert file_output.get_file_name() == "name"
    assert file_output.stream.close.called is True


@mock.patch("drf_viewset_profiler.output.output_default_location", "/some/other/location/")
@mock.patch("builtins.open")
def test_file_output_with_another_output_location(mock_open):
    file_output = FileOutput("name")

    assert file_output.get_file_name() == "/some/other/location/name"
    assert mock_open.call_args_list[0] == mock.call("/some/other/location/name", "w")

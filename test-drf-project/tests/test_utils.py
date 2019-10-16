import pytest

from drf_viewset_profiler.utils import create_line_profile, get_value_from_config


class SomeClass:
    attr = None

    def __str__(self):
        return "SomeClass"

    def _attr_0(self):
        pass

    def attr_1(self):
        pass

    @property
    def attr_2(self):
        pass

    @staticmethod
    def attr_3():
        pass

    @classmethod
    def attr_4(cls):
        pass


class SomeAnotherClass:
    attr = None

    def __str__(self):
        return "SomeClass"

    def _attr_0(self):
        pass

    def attr_1(self):
        pass


def test_create_line_profile_with_class():
    line_profiler = create_line_profile(SomeClass)
    functions = line_profiler.functions

    assert SomeClass.attr not in functions
    assert SomeClass.__str__ in functions
    assert SomeClass._attr_0 in functions
    assert SomeClass.attr_1 in functions
    assert SomeClass.attr_2 not in functions
    assert SomeClass.attr_3 in functions
    assert SomeClass.attr_4 in functions


def test_create_line_profile_with_more_than_one_class():
    line_profiler = create_line_profile(SomeClass, SomeAnotherClass)
    functions = line_profiler.functions

    assert SomeClass.attr not in functions
    assert SomeClass.__str__ in functions
    assert SomeClass._attr_0 in functions
    assert SomeClass.attr_1 in functions
    assert SomeClass.attr_2 not in functions
    assert SomeClass.attr_3 in functions
    assert SomeClass.attr_4 in functions

    assert SomeAnotherClass.attr not in functions
    assert SomeAnotherClass.__str__ in functions
    assert SomeAnotherClass._attr_0 in functions
    assert SomeAnotherClass.attr_1 in functions


def test_create_line_profile_with_function():
    line_profiler = create_line_profile(lambda: True)

    assert len(line_profiler.functions) == 0


def test_get_value_from_config_without_existing_config():
    assert get_value_from_config("foo", "bar") == "bar"


@pytest.mark.parametrize(
    "config,expected",
    (
        ("DEFAULT_OUTPUT_GENERATION_TYPE", "drf_viewset_profiler.output.StdOutput"),
        ("DEFAULT_OUTPUT_LOCATION", ""),
        ("ENABLE_SERIALIZER_PROFILER", True),
    ),
)
def test_get_value_from_config_with_existing_config(config, expected):
    assert get_value_from_config(config, "") == expected

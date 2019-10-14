from drf_viewset_profiler.utils import create_line_profile


def test_create_line_profile_with_class():
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

    line_profiler = create_line_profile(SomeClass)
    functions = line_profiler.functions

    assert SomeClass.attr not in functions
    assert SomeClass.__str__ in functions
    assert SomeClass._attr_0 in functions
    assert SomeClass.attr_1 in functions
    assert SomeClass.attr_2 not in functions
    assert SomeClass.attr_3 in functions
    assert SomeClass.attr_4 in functions


def test_create_line_profile_with_function():
    line_profiler = create_line_profile(lambda: True)

    assert len(line_profiler.functions) == 0

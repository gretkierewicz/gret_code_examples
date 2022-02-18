"""
conversion utilities testing module
"""
# pylint: disable-all
import pytest

from .. import turn_into_floats


class TestTurnIntoFloats:
    def test_turn_zeroes(self):
        _list = [0] * 5
        assert _list == turn_into_floats(*_list)

    def test_turn_integer_range(self):
        _list = list(range(6))
        assert _list == turn_into_floats(*_list)

    def test_turn_proper_string_range(self):
        _list = list(range(6))
        assert _list == turn_into_floats(*[str(i) for i in _list])

    def test_wrong_string_passed(self):
        with pytest.raises(ValueError) as excinfo:
            turn_into_floats(*["not_a_number", 1, 2])
        assert "could not convert string" in str(excinfo.value)

    def test_no_args(self):
        assert turn_into_floats() == []

    def test_zeroed_limit_without_args(self):
        assert turn_into_floats(output_count=0) == []

    def test_zeroed_limit_with_args(self):
        assert turn_into_floats(1, 2, 3, output_count=0) == [1, 2, 3]

    def test_negative_limit(self):
        assert turn_into_floats(1, 2, 3, output_count=-1) == []

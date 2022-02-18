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
        _list = [i for i in range(6)]
        assert _list == turn_into_floats(*_list)

    def test_turn_proper_string_range(self):
        _list = [i for i in range(6)]
        assert _list == turn_into_floats(*[str(i) for i in _list])

    def test_wrong_string_passed(self):
        with pytest.raises(ValueError) as excinfo:
            turn_into_floats(*["not_a_number", 1, 2])
        assert "could not convert string" in str(excinfo.value)

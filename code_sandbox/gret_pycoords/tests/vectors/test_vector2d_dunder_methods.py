"""
Vector2D dunder methods testing module
"""
# pylint: disable-all
from ... import Vector2D


class TestGettingItem:
    def test_empty(self):
        vec = Vector2D()
        assert vec[0] == 0
        assert vec[1] == 0

    def test_int_zeroed(self):
        vec = Vector2D(0, 0)
        assert vec[0] == 0
        assert vec[1] == 0

    def test_float_zeroed(self):
        vec = Vector2D(0.0, 0.0)
        assert vec[0] == 0
        assert vec[1] == 0

    def test_custom_values(self):
        vec = Vector2D(1.2, -0.21)
        assert vec[0] == 1.2
        assert vec[1] == -0.21

    def test_one_arg(self):
        vec = Vector2D(1.2)
        assert vec[0] == 1.2
        assert vec[1] == 0

    def test_slicing_whole_vector(self):
        assert Vector2D(1.2, -2.1)[:] == [1.2, -2.1]

    def test_slicing_whole_vector_with_unpacking_args(self):
        args = [1.2, -2.1]
        assert Vector2D(*args)[:] == args

    def test_slicing_whole_vector_with_unpacking_short_args(self):
        args = [1.2]
        assert Vector2D(*args)[:] == args + [0]

    def test_slicing_whole_vector_with_unpacking_long_args(self):
        args = [1.2, -2.1, 321, 0, 1]
        assert Vector2D(*args)[:] == args[:2]


class TestSettingItem:
    def test_setting_float_values_by_indexes(self):
        vec = Vector2D()
        vec[0] = 1.2
        vec[1] = -0.3
        assert vec[:] == [1.2, -0.3]

    def test_setting_int_values_by_indexes(self):
        vec = Vector2D()
        vec[0] = 12
        vec[1] = -32
        assert vec[:] == [12, -32]

    def test_setting_list_to_slice_of_full_vector(self, args2d):
        vec = Vector2D()
        vec[:] = args2d
        assert vec[:] == args2d

    def test_setting_list_to_slice_for_first_element(self):
        vec = Vector2D(0, -2.1)
        vec[:1] = [1.2]
        assert vec[:] == [1.2, -2.1]

    def test_setting_list_to_slice_for_second_element(self):
        vec = Vector2D(1.2, 0)
        vec[1:] = [-2.1]
        assert vec[:] == [1.2, -2.1]

    def test_swapping_values_with_slicing(self, args2d, vec2d):
        assert vec2d[::-1] == args2d[::-1]

    def test_setting_longer_list_to_full_slice(self):
        vec = Vector2D()
        vec[:] = [1, 2, 3]
        assert vec[:] == [1, 2]

    def test_setting_long_list_to_first_element_slice(self):
        vec = Vector2D()
        vec[:1] = [1, 2, 3]
        assert vec[:] == [1, 0]

    def test_setting_long_list_to_second_element_slice(self):
        vec = Vector2D()
        vec[1:] = [1, 2, 3]
        assert vec[:] == [0, 1]

    def test_setting_short_list_to_full_slice(self):
        vec = Vector2D()
        vec[:] = [1]
        assert vec[:] == [1, 0]


class TestEquality:
    def test_vector_equals_to_itself(self, vec2d):
        assert vec2d == vec2d

    def test_same_value_vectors_equals(self, args2d):
        assert Vector2D() == Vector2D()
        assert Vector2D(*args2d) == Vector2D(*args2d)

    def test_vector_equals_to_list_of_same_values(self, args2d):
        assert Vector2D(*args2d) == args2d
        assert Vector2D() == [0, 0]

    def test_vector_equals_to_tuple_of_same_values(self, args2d):
        assert Vector2D(*args2d) == tuple(args2d)
        assert Vector2D() == (0, 0)

    def test_vectors_not_equal_if_values_differ(self, vec2d):
        assert Vector2D() != Vector2D(1)
        assert Vector2D() != Vector2D(0, 1)
        assert Vector2D() != vec2d
        assert Vector2D(1) != Vector2D(0, 1)
        assert Vector2D(1) != vec2d
        assert Vector2D(0, 1) != vec2d

    def test_never_equal_to_not_iterable_of_numbers_of_len_2(self, vec2d):
        assert vec2d != "some string"
        assert Vector2D() != [0]
        assert Vector2D() != 0
        assert Vector2D() != 0.0

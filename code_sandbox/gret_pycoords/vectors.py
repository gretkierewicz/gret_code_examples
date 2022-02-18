"""
Vectors module
"""

__all__ = [
    "Vector2D",
]

from typing import Any, List, Sequence, Sized, Union

from .. import utils


class Vector2D:
    """
    Vector class for 2 dimensional space
    """

    _data: List[float]

    def __init__(self, *args: float) -> None:

        self._data = utils.turn_into_floats(*args, output_count=len(self))

    def __getitem__(self, idx: int) -> float:
        return self._data.__getitem__(idx)

    def __setitem__(self, key: Union[int, slice], value: Any):
        if isinstance(key, slice):
            slice_len = len(self._data[key])
            value = utils.turn_into_floats(*value, output_count=slice_len)
        else:
            value = float(value)

        self._data.__setitem__(key, value)

    def __len__(self):
        return 2

    def __eq__(self, other: Union[Sequence, Sized]) -> bool:
        try:
            if len(other) != 2:
                return False
        except TypeError:
            return False

        return all(self[i] == other[i] for i in range(len(self)))

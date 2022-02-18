"""
Conversion utilities module
"""

__all__ = [
    "turn_into_floats",
]

from typing import Any, List


def turn_into_floats(*args: Any, output_count: int = 0) -> List[float]:
    """
    Function will convert arguments into list of floats. If output count is given, list
    will get fixed length (sliced or filled with zeroes).

    :param args: Arguments to convert
    :param output_count: Optional param for setting list's fixed length. Default value is
        0 for converting the whole list of args.
    :return: List of arguments converted into floats
    """

    if output_count < 0:
        return []

    numbers = [float(arg) for arg in args]
    if output_count and len(numbers) < output_count:
        numbers += [0] * output_count
    if output_count and len(numbers) > output_count:
        numbers = numbers[:output_count]
    return numbers

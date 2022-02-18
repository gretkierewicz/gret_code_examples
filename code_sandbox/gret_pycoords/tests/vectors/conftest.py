"""
vectors configuration for tests
"""
# pylint: disable-all
from typing import List

import pytest

from ... import Vector2D


@pytest.fixture
def args2d() -> List[float]:
    """List of 2 args, each different than 0"""
    return [1.2, -2.1]


@pytest.fixture
def vec2d(args2d) -> Vector2D:
    """Vector2d with values of args2d fixture"""
    return Vector2D(*args2d)

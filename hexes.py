"""Contains data for building hexagonal maps."""

from collections import namedtuple
from dataclasses import dataclass
from functools import cached_property

from math import sqrt, sin, cos
from math import pi as PI

Vector = namedtuple("Vector", "x y")


@dataclass(frozen=True)
class HexTile:
    """Basic component of a hex map.
       This hex implementation is pointy-topped."""

    _x_position: float = 0
    _y_position: float = 0
    _size: float = 30

    @cached_property
    def corners(self):
        """Calculate all corners for a hex."""
        for num_corner in range(6):
            angle_degrees = 60 * num_corner + 30
            angle_rad = PI / 180 * angle_degrees
            # TODO Consider casting to int first.
            yield Vector(
                self._x_position + self._size * cos(angle_rad),
                self._y_position + self._size * sin(angle_rad))

    @cached_property
    def width(self):
        """Calculate hex's width."""
        # sqrt(3) comes from sin of 60 degrees.
        return sqrt(3) * self._size

    @cached_property
    def height(self):
        """Calculate hex's height."""
        return 2 * self._size

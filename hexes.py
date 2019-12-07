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
        """Return list of this hex's corners."""
        return [Vector(int(x), int(y))
                for x, y in self._get_corners()]

    def _get_corners(self):
        """Calculate all corners for this hextile."""
        for num_corner in range(6):
            # Each corner is 60 degrees apart from the next one.
            angle_degrees = 60 * num_corner + 30
            angle_rad = PI / 180 * angle_degrees
            # Calculate 6 points by drawing 6 lines from the center.
            # Lines' length are determined by hextile's size.
            yield (self._x_position + self._size * cos(angle_rad),
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
"""Contains data for building hexagonal maps."""

from collections import namedtuple
from dataclasses import dataclass, field
from functools import cached_property
from typing import List, Generator, Tuple

from math import sqrt, sin, cos
from math import pi as PI

from hex_types import HexType

Point = namedtuple("Point", "x_position y_position")
AxialCoords = namedtuple("AxialCoords", "q_axis r_axis")
CubeCoords = namedtuple("CubeCoods", "x_axis y_axis z_axis")
DoubledCoords = namedtuple("DoubledCoords", "x_offset y_offset")


@dataclass
class HexTile:
    """Basic component of a hex map.
       This hex implementation is pointy-topped."""

    _x_position: float = 0
    _y_position: float = 0
    _size: float = 30

    _offsetx: int = 0
    _offsety: int = 0

    _type: HexType = field(default=HexType.Sea)

    @cached_property
    def corners(self) -> Tuple[Point]:
        """Return tuple of this hex's corners."""
        return tuple((Point(round(x), round(y))
                      for x, y in self._get_corners()))

    def _get_corners(self) -> Generator[Point, None, None]:
        """Calculate all six corners for this hextile."""
        for num_corner in range(6):
            # Each corner is 60 degrees apart from the next one.
            angle_degrees = 60 * num_corner + 30
            angle_rad = PI / 180 * angle_degrees
            # Calculate 6 points by drawing 6 lines from the center.
            # Lines' length are determined by hextile's size.
            yield Point(self._x_position + self._size * cos(angle_rad),
                        self._y_position + self._size * sin(angle_rad))

    @cached_property
    def position(self) -> Point:
        """Return tile's position on the screen."""
        return Point(self._x_position, self._y_position)

    @cached_property
    def width(self) -> float:
        """Calculate hex's width."""
        # sqrt(3) comes from sin of 60 degrees.
        return sqrt(3) * self._size

    @cached_property
    def height(self) -> float:
        """Calculate hex's height."""
        return 2 * self._size

    @cached_property
    def doubled(self) -> DoubledCoords:
        """This tile's doubled offset coordinates."""
        return DoubledCoords(self._offsetx, self._offsety)

    @cached_property
    def axial(self) -> AxialCoords:
        """This tile's axial coordinates, converted from doubled."""
        return HexTile.doubled2axial(self.doubled)

    @property
    def type(self) -> HexType:
        return self._type

    @type.setter
    def type(self, new_type: HexType) -> None:
        self._type = new_type

    # Conversion methods for coordinates.

    @staticmethod
    def axial2doubled(coordinates: AxialCoords) -> DoubledCoords:
        q, r = coordinates
        # Doubled base vectors are (0, 2) and (1, 1)
        return DoubledCoords(2*q + r, r)

    @staticmethod
    def doubled2axial(coordinates: DoubledCoords) -> AxialCoords:
        x, y = coordinates
        q, r = (x - y)//2, y
        return AxialCoords(q, r)

    @staticmethod
    def axial2cube(coordinates: AxialCoords) -> CubeCoords:
        """Convert hex's axial coordinates (q, r)
            to cube coordinates (x, y, z)."""
        q_axis, r_axis = coordinates

        # Required ratio of q + r + s = 0
        s_axis = -q_axis - r_axis
        return CubeCoords(q_axis, r_axis, s_axis)

    @staticmethod
    def cube2axial(coordinates: CubeCoords) -> AxialCoords:
        """Convert hex's cube coordinates (x, y, z)
            to axial coordinates (q, r)."""
        # Discard the z coordinate.
        return AxialCoords(*coordinates[:2])

    @staticmethod
    def round_cube(coordinates: CubeCoords) -> CubeCoords:
        """Round cube coordinates to the nearest hex.
           The result is (x, y, z) integer coordinates."""
        # Round all coordinates to int values.
        round_coords = [round(axis) for axis in coordinates]
        x_round, y_round, z_round = round_coords

        # Calculate differences made when rounding, for each axis.
        x_diff, y_diff, z_diff = (
            abs(original - round_)
            for original, round_ in zip(coordinates, round_coords)
        )

        # Find biggest difference of them; recalculate value for that axis.
        # Maintain the ratio of (x + y + z = 0).
        if x_diff > y_diff and x_diff > z_diff:
            x_round = -y_round - z_round
        elif y_diff > z_diff:
            y_round = -x_round - z_round
        else:
            z_round = -x_round - y_round

        return CubeCoords(x_round, y_round, z_round)

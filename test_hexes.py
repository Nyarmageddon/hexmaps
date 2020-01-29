"""Tests for hexes and coordinates methods."""

from dataclasses import FrozenInstanceError
from typing import Tuple

import pytest

from hexes import HexTile, AxialCoords, CubeCoords, Point

Doubled = Tuple[int]


@pytest.fixture
def default_hex() -> HexTile:
    return HexTile()


@pytest.fixture
def hex_100_size() -> HexTile:
    return HexTile(_size=100)


def test_hex_init(default_hex: HexTile, hex_100_size: HexTile):
    assert isinstance(default_hex, HexTile)
    assert default_hex._x_position == 0
    assert default_hex._y_position == 0
    assert hex_100_size._size == 100


def test_frozen(default_hex: HexTile, hex_100_size: HexTile):
    with pytest.raises(FrozenInstanceError):
        hex_100_size._size = 200
    with pytest.raises(FrozenInstanceError):
        default_hex._x_position = 50


def test_corners(hex_100_size: HexTile):
    corners = hex_100_size.corners
    assert isinstance(corners, list)
    assert len(corners) == 6
    for corner in corners:
        assert isinstance(corner, Point)


@pytest.mark.parametrize(
    "position, size, expected",
    [
        ((0, 0), 100, [(87, 50), (0, 100), (-87, 50),
                       (-87, -50), (0, -100), (87, -50)]),

        ((200, 200), 50, [(243, 225), (200, 250), (157, 225),
                          (157, 175), (200, 150), (243, 175)]),
    ])
def test_corner_math(position, size, expected):
    # Prepare a hex tile for testing.
    x, y = position
    hex_tile = HexTile(_x_position=x, _y_position=y, _size=size)

    for corner in hex_tile.corners:
        (x, y) = corner
        assert (x, y) in expected


def test_width_height(hex_100_size: HexTile):
    assert round(hex_100_size.height) == 200
    assert round(hex_100_size.width) == 173


# Coordinate convertion tests.

doubled = [
    (0, 0),
    (2, 0),
    (1, 1),
    (3, 1),
    (-4, 0),
    (15, 5),
]

axial = [
    AxialCoords(0, 0),
    AxialCoords(1, 0),
    AxialCoords(0, 1),
    AxialCoords(1, 1),
    AxialCoords(-2, 0),
    AxialCoords(5, 5),
]

cube = [
    CubeCoords(0, 0, 0),
    CubeCoords(1, 0, -1),
    CubeCoords(0, 1, -1),
    CubeCoords(1, 1, -2),
    CubeCoords(-2, 0, 2),
    CubeCoords(5, 5, -10),
]


@pytest.mark.parametrize(
    "doubled, expected", zip(doubled, axial)
)
def test_axial(doubled: Doubled, expected: AxialCoords):
    x, y = doubled
    hex_tile = HexTile(_offsetx=x, _offsety=y)
    assert hex_tile.axial == expected


@pytest.mark.parametrize(
    "axial, cube", zip(axial, cube)
)
def test_axial_cube_conversion(axial: AxialCoords, cube: CubeCoords):
    assert HexTile.axial2cube(axial) == cube
    assert HexTile.cube2axial(cube) == axial

"""Data and algorithms for hexagonal maps for strategy/tactics games.
   Reference: https://www.redblobgames.com/grids/hexagons/#conversions-doubled
"""

from dataclasses import dataclass, field
from itertools import product
from math import sqrt
from random import randint
from typing import Iterator, List

from hexes import HexTile, Point, AxialCoords, DoubledCoords
from hex_types import HexType

# 6 directions in doubled coordinates to search for hex's neighbors.
NEIGHBOR_DIRECTIONS = (
    (2, 0),
    (1, 1),
    (-1, 1),
    (-2, 0),
    (-1, -1),
    (1, -1)
)


@dataclass
class HexMap():
    """Rectangular-shaped array of hexagons.
       Indexing starts at the top-left corner."""

    # Map's dimensions in hexes.
    _width: int
    _height: int

    _hex_size: float = 50

    # Position of top-left tile the map starts from.
    _first_hex: Point = field(default_factory=tuple)
    _hexes: List[HexTile] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Generate hexmap's contents if none were provided."""
        if not self._hexes:
            self._hexes = HexMap._generate_hexes(self._width, self._height,
                                                 *self._first_hex,
                                                 hex_size=self._hex_size,)

            self._first_hex = self._hexes[0].position

    def __iter__(self) -> Iterator[HexTile]:
        return iter(self._hexes)

    def get_hex(self, *coordinates) -> HexTile:
        """Get hex with given doubled coordinates, or None if not in this map.
           Supports either singular argument with two coordinates in it,
           or two int arguments."""
        if len(coordinates) == 1:
            orig_x, orig_y = coordinates[0]
        elif len(coordinates) == 2:
            orig_x, orig_y = coordinates
        else:
            raise TypeError("Need to provide coordinates of a given hex.")

        x = orig_x // 2  # Remove the doubling of X-coordinates

        # Check for map boundaries
        if x < 0 or x >= self._width or orig_y < 0 or orig_y >= self._height:
            return None

        # Convert 2D coordinates to flat list index.
        hex_index = orig_y * self._width + x
        try:
            found_hex = self._hexes[hex_index]
        except IndexError:
            return None

        # Validate coordinates to verify we found the correct tile.
        # This filters out invalid coordinates, for example (1, 0).
        found_x, found_y = found_hex.doubled
        if (orig_x, orig_y) != (found_x, found_y):
            return None
        else:
            return found_hex

    def find_by_axial(self, coords: AxialCoords) -> HexTile:
        """Find and return a hex tile by its axial coordinates,
           or None if no hex was found."""
        for hex_tile in self._hexes:
            if hex_tile.axial == coords:
                return hex_tile

    def find_neighbors(self, hex_tile: HexTile) -> List[HexTile]:
        """Find given tile's neighbors on this map."""
        tile_coords = hex_tile.doubled

        # Try finding neighbors in all 6 directions.
        neighbor_coords = []
        for neighbor_offset in NEIGHBOR_DIRECTIONS:
            # Add together base coordinates and vectors to 6 neighbors.
            result = DoubledCoords(*(sum(pair)
                                     for pair in zip(tile_coords, neighbor_offset)))
            neighbor_coords.append(result)

        # Return all neighboring hexes by searching their coordinates.
        return [
            self.get_hex(coords)
            for coords in neighbor_coords
            if self.get_hex(coords)
        ]

    def pixel2hex(self, pixel_x: float, pixel_y: float) -> HexTile:
        """Find hex in this map by pixel location (i.e. a mouse click)."""
        # First find coordinates without the initial offset from top-left.
        base_x, base_y = self._first_hex
        x = pixel_x - base_x
        y = pixel_y - base_y

        # Find hex's position in (q, r) axis.
        # Math src: https://www.redblobgames.com/grids/hexagons/#pixel-to-hex
        q_axis = (sqrt(3)/3 * x - 1/3 * y) / self._hex_size
        r_axis = (2/3 * y) / self._hex_size

        # Convert coords axial -> cube, round them to the closest hex,
        #  convert from cube back to axial and then to doubled 0_0.
        coords = HexTile.axial2doubled(HexTile.cube2axial(
            HexTile.round_cube(HexTile.axial2cube((q_axis, r_axis)))))

        return self.get_hex(coords)

    # TODO think of correct place to put this method in.
    @staticmethod
    def _generate_hexes(width: int, height: int,
                        initial_x: float = 0, initial_y: float = 0,
                        hex_size: float = 50) -> List[HexTile]:
        """Generate a hexmap of size (width x height) in hexes."""
        # Create one tile to use its measurements later on.
        tile = HexTile(initial_x, initial_y, hex_size)

        tiles = []
        for n_row, n_column in product(range(height), range(width)):
            # Offset hexes to the right in odd rows.
            offset = 0.5 * tile.width if n_row % 2 == 1 else 0

            # Vertical space is smaller than tile's full height for hexes.
            vertical_space = tile.height * 0.75

            tiles.append(
                HexTile(
                    initial_x + n_column * tile.width + offset,
                    initial_y + n_row * vertical_space,
                    hex_size,
                    # Set up even X-coordinates for even rows by doubling.
                    # In odd rows, offset them by 1.
                    n_column * 2 + (1 if offset else 0),
                    n_row,
                    HexType.Sea if randint(0, 1) == 0 else HexType.Land
                )
            )
        return tiles

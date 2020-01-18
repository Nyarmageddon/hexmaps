"""Data and algorithms for hexagonal maps for strategy/tactics games.
   Reference: https://www.redblobgames.com/grids/hexagons/#conversions-doubled
"""

from dataclasses import dataclass, field
from itertools import product
from math import sqrt
from typing import Iterator, List

from hexes import HexTile, Point, AxialCoords


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

    def find_by_axial(self, coords: AxialCoords) -> HexTile:
        """Find and return a hex tile by its axial coordinates,
           or None if no hex was found."""
        for hex_tile in self._hexes:
            if hex_tile.axial == coords:
                return hex_tile

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
        #  convert coords from cube back to axial.
        coords = HexTile.cube2axial(
            HexTile.round_cube(HexTile.axial2cube((q_axis, r_axis))))

        return self.find_by_axial(coords)

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
                    n_row
                )
            )
        return tiles

"""Data and algorithms for hexagonal maps for strategy/tactics games.
   Reference: https://www.redblobgames.com/grids/hexagons/#conversions-doubled
"""

from dataclasses import dataclass, field
from itertools import product
from typing import List

from hexes import HexTile, Point


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

    def __post_init__(self):
        """Generate hexmap's contents if none were provided."""
        if not self._hexes:
            self._hexes = HexMap._generate_empty_map(self._width, self._height)
            self._first_hex = self._hexes[0].position

    def __iter__(self):
        return iter(self._hexes)

    # TODO think of correct place to put this method in.
    # The idea is to put it into a hex_map.generator module.
    @staticmethod
    def _generate_empty_map(width: int, height: int,
                            initial_x: float = 200, initial_y: float = 200,
                            tile_size: float = 50):
        """Generate a hexmap of size (width x height) in hexes."""
        # Create one tile to use its measurements later on.
        tile = HexTile(initial_x, initial_y, tile_size)

        tiles = []
        for n_row, n_column in product(range(height), range(width)):
            # Offset hexes to the left every other row.
            offset = -0.5 * tile.width if n_row % 2 == 0 else 0

            # Vertical space is smaller than tile's full height for hexes.
            vertical_space = tile.height * 0.75

            tiles.append(
                HexTile(
                    initial_x + n_column * tile.width + offset,
                    initial_y + n_row * vertical_space,
                    tile_size,
                    n_column * 2,  # Doubled coordinates for columns
                    n_row
                )
            )
        return tiles

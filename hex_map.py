"""Data and algorithms for hexagonal maps for strategy/tactics games.
   Reference: https://www.redblobgames.com/grids/hexagons/#conversions-doubled
"""

from dataclasses import dataclass, field
from hexes import HexTile
from itertools import product
from typing import List


@dataclass
class HexMap():
    """Rectangular-shaped array of hexagons."""

    _width: int
    _height: int
    _hex_size: float = 50

    _hexes: List[HexTile] = field(default_factory=list)

    def __post_init__(self):
        """Generate hexmap's contents if none were provided."""
        if not self._hexes:
            self._hexes = HexMap._generate_empty_map(self._width, self._height)

    # TODO think of correct place to put this method in.
    @staticmethod
    def _generate_empty_map(width, height):
        """Generate a hexmap of size (width x height) in hexes."""
        initial_x, initial_y = (200, 200)
        tile_size = 50
        tile = HexTile(initial_x, initial_y, tile_size)

        tiles = []
        for n_row, n_column in product(range(height), range(width)):
            # Offset hexes to the left every other row.
            offset = 0.5 * tile.width if n_row % 2 == 0 else 0

            tiles.append(
                HexTile(
                    initial_x + n_column * tile.width - offset,
                    initial_y + n_row * tile.height * 0.75,
                    tile_size)
            )
        return tiles

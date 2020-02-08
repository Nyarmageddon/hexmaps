"""Contains data to distinguish between different types of tiles."""

from enum import Enum


class HexType(Enum):

    Sea = 0,
    Land = 1,

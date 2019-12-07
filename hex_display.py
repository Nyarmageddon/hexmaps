"""Front-end to draw the hexmaps to pygame window."""

import pygame

from hexes import HexTile
from hex_map import HexMap
from random import randint

# TODO Move these to some kind of config.
SCREEN_RESOLUTION = (1200, 800)
BG_COLOR = (245, 222, 179)
BASE_TILE_COLOR = (205, 133, 63)


def run_graphics():
    """Initialize Pygame window."""
    # Initialize Pygame window, fill it with solid color.
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    screen.fill(color=BG_COLOR)

    _draw_map(screen)

    # Main loop.
    while True:
        # Exit on Escape or Q press.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    exit()

        # Update the screen.
        pygame.display.flip()


# TODO move color management to separate module.
def _modify_color(color):
    """Apply a small change to the given color."""
    color_delta = tuple(randint(-30, 30) for _ in range(3))
    return tuple(sum(color_components)
                 for color_components in zip(color, color_delta)
                 )


def _draw_map(screen):
    """Draw the entire map on the screen."""
    my_map = HexMap(8, 8)
    for tile in my_map._hexes:
        # print(tile)
        pygame.draw.polygon(screen, _modify_color(BASE_TILE_COLOR),
                            list(tile.corners))


def _draw_hex(screen):
    """Draw one hex on the screen."""
    # Initialize the first hex and calculate its corners.
    my_tile = HexTile(350, 350, 50)
    corners = [(int(x), int(y))
               for x, y in my_tile.corners]
    # Draw the hex.
    pygame.draw.polygon(screen, BASE_TILE_COLOR, corners)


if __name__ == "__main__":
    run_graphics()

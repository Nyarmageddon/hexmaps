"""Front-end to draw the hexmaps to Pygame window."""

from random import randint

import pygame

from hexes import HexTile
from hex_map import HexMap

# TODO Move these to some kind of config.
SCREEN_RESOLUTION = (1200, 800)
BG_COLOR = (245, 222, 179)
BASE_TILE_COLOR = (205, 133, 63)


def run_graphics():
    """Use Pygame to draw hex maps."""
    # Initialize Pygame window, fill it with solid color.
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    screen.fill(color=BG_COLOR)

    _draw_map(screen)

    # Main loop.
    while True:
        # React to user actions, such as key presses.
        _handle_events(screen)

        # Update the screen.
        pygame.display.flip()


def _handle_events(screen):
    """React to user actions, such as key presses."""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Exit on Escape or Q press.
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                exit()
            # Redraw the map on R press.
            elif event.key == pygame.K_r:
                _draw_map(screen)


# TODO move color management to separate module.
def _modify_color(color):
    """Apply a small change to the given color."""
    return tuple(color_component + randint(-30, 30)
                 for color_component in color)


def _draw_map(screen):
    """Draw a grid of hexes on the screen."""
    my_map = HexMap(8, 8)
    for tile in my_map._hexes:
        # print(tile)
        tile_color = _modify_color(BASE_TILE_COLOR)
        pygame.draw.polygon(screen, tile_color, tile.corners)


def _draw_hex(screen):
    """Draw one hex on the screen."""
    # Initialize one hex and draw it on the screen.
    my_tile = HexTile(350, 350, 50)
    pygame.draw.polygon(screen, BASE_TILE_COLOR, my_tile.corners)


if __name__ == "__main__":
    run_graphics()

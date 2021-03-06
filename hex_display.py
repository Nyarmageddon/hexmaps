"""Front-end to draw the hexmaps to Pygame window."""

from random import randint

import pygame

from hex_types import HexType
from hexes import HexTile
from hexmaps import HexMap

# TODO Move these to some kind of config.
SCREEN_RESOLUTION = (1200, 800)
BG_COLOR = (245, 222, 179)
COLORS = {
    HexType.Land: (205, 133, 63),
    HexType.Sea: (64, 135, 206),
}


def run_graphics():
    """Use Pygame to draw hex maps."""
    # Initialize Pygame window, fill it with solid color.
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RESOLUTION)
    pygame.display.set_caption("Nyarmageddon's Hexmaps")
    screen.fill(color=BG_COLOR)

    my_map = _draw_map(screen)

    # Main loop.
    while True:
        # React to user actions, such as key presses.
        _handle_events(screen, my_map)

        # Update the screen.
        pygame.display.flip()


def _handle_events(screen, hexmap: HexMap):
    """React to user actions, such as key presses."""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Exit on Escape or Q press.
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                exit()
            # Redraw the map on R press.
            elif event.key == pygame.K_r:
                _draw_map(screen)
        # Print hex's coordinates on click.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # LMB press
                tile = hexmap.pixel2hex(*event.pos)
                if tile:
                    x, y = tile.doubled
                    print(f"Clicked tile at {(x, y)}. Neighbors:")
                    neighbors = hexmap.find_neighbors(tile)
                    for neighbor in neighbors:
                        x, y = neighbor.doubled
                        print((x, y))
                    print()


# TODO move color management to separate module.
def _modify_color(color):
    """Apply a small change to the given color."""
    return tuple(color_component + randint(-20, 20)
                 for color_component in color)


def _draw_map(screen):
    """Draw a grid of hexes on the screen."""
    my_map = HexMap(80, 80, _hex_size=10)
    my_map.generate_with_random_walk(150, iterations=25)
    for tile in my_map:
        # print(tile)
        color = COLORS[tile.type]

        tile_color = _modify_color(color)
        pygame.draw.polygon(screen, tile_color, tile.corners)
    return my_map


def _draw_hex(screen):
    """Draw one hex on the screen."""
    # Initialize one hex and draw it on the screen.
    my_tile = HexTile(350, 350, 50)
    pygame.draw.polygon(screen, COLORS[HexType.Land], my_tile.corners)


if __name__ == "__main__":
    run_graphics()

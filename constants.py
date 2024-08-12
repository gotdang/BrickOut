from pathlib import Path
# import pygame
# import pygame.freetype
# from random import choice, Random, seed
# from signum import signum
from named_colors import named_colors

if True:  # force window to upper left corner during development.
    import os
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"

# Globals
COLOR = 255, 100, 98
SURFACE_COLOR = named_colors["grayf"]
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

image_dir = Path(r"C:\Users\Dang\Pictures\Digital Blasphemy")
BG_IMAGES = tuple(Path(image_dir).glob("*.jpg"))


# Initialize static stuff
BRICKS_X_COUNT = 14
BRICK_WIDTH = (SCREEN_WIDTH - 20) // BRICKS_X_COUNT
BRICK_HEIGHT = 20
ABOVE_BRICKS = 3 * BRICK_HEIGHT  # Keep an open space above the bricks.
BRICK_LEFT = (SCREEN_WIDTH - BRICKS_X_COUNT * BRICK_WIDTH) // 2
BRICK_COLOR = 255, 255, 255
BRICK_BORDER_COLOR = named_colors["gray4"]

BALL_RADIUS = 20

LEFT_MARGIN = (SCREEN_WIDTH - BRICKS_X_COUNT * BRICK_WIDTH) // 2 - 1
RIGHT_MARGIN = SCREEN_WIDTH - LEFT_MARGIN - 1

BACKGROUND_COLOR = named_colors["gray2"]
MARGIN_COLOR = named_colors["white"]

# 8 colors
BRICK_LAYER_COUNT = 8
BRICK_COLORS = [
    named_colors["hotpink"],
    named_colors["red"],
    # named_colors["brown"],
    named_colors["orange"],
    named_colors["yellow"],
    named_colors["green"],
    named_colors["blue"],
    named_colors["rebeccapurple"],
    named_colors["cyan"],
]
assert len(BRICK_COLORS) >= BRICK_LAYER_COUNT, "Not enough colors for the bricks."

PADDLE_COLOR = named_colors["brown"]
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BELOW_PADDLE = 1 * PADDLE_HEIGHT


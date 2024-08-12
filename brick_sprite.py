import pygame
from constants import BRICK_WIDTH, BRICK_HEIGHT, BRICK_LEFT, ABOVE_BRICKS, BRICK_COLORS, BRICK_BORDER_COLOR
from game_sprite import GameSprite
from named_colors import named_colors
from random import choice


class BrickSprite(GameSprite):
    def __init__(self, x, y):
        super().__init__(choice(list(named_colors.values())), BRICK_WIDTH, BRICK_HEIGHT)
        # The incoming x, y are brick coordinates, not screen coordinates.
        self.rect = pygame.Rect(
            BRICK_LEFT + x * BRICK_WIDTH,
            ABOVE_BRICKS + y * BRICK_HEIGHT,
            BRICK_WIDTH,
            BRICK_HEIGHT,
        )
        self.color = BrickSprite.layer_color(self.rect)
        pyrect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.image, self.color, pyrect)
        pygame.draw.rect(self.image, BRICK_BORDER_COLOR, pyrect, 2)

    @staticmethod
    def layer_color(brick: pygame.Rect) -> tuple:
        brick_layer = (brick.y - ABOVE_BRICKS) // BRICK_HEIGHT
        return BRICK_COLORS[brick_layer]



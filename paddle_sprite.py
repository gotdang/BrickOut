import pygame
from constants import SCREEN_HEIGHT, LEFT_MARGIN, RIGHT_MARGIN, PADDLE_COLOR, PADDLE_WIDTH, PADDLE_HEIGHT
from game_sprite import GameSprite


class PaddleSprite(GameSprite):
    def __init__(self, color=PADDLE_COLOR, width=PADDLE_WIDTH, height=PADDLE_HEIGHT):
        super().__init__(color, width, height)

    def handle_event(self, keys):
        if keys[pygame.K_LEFT]:
            self.moveLeft(10)
        if keys[pygame.K_RIGHT]:
            self.moveRight(10)

    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x + self.width > RIGHT_MARGIN:
            self.rect.x = RIGHT_MARGIN - self.width

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        if self.rect.x <= LEFT_MARGIN:
            self.rect.x = 1 + LEFT_MARGIN

    def moveForward(self, speed):
        self.rect.y -= self.height
        if self.rect.y < 0:
            self.rect.y = 0

    def moveBackward(self, speed):
        self.rect.y += self.height
        if self.rect.y + self.height > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.height



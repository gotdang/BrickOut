import pygame
from constants import SCREEN_HEIGHT, LEFT_MARGIN, RIGHT_MARGIN, BRICK_HEIGHT, BRICK_LAYER_COUNT, ABOVE_BRICKS, DEMO
from game_sprite import GameSprite
from random import choice
from signum import signum
import sounds


class BallSprite(GameSprite):
    x_speeds = (5, 10, 15)
    y_speeds = (2, 3, 4)

    def __init__(self, color, radius, glob, paddle_sprite, brick_sprites):
        super().__init__(color, radius, radius)
        self.radius = radius
        self.dx = choice((-1, 1)) * self.x_speeds[len(self.x_speeds) // 2]
        self.dy = self.y_speeds[len(self.y_speeds) // 2]
        self.glob = glob
        self.paddle_sprite = paddle_sprite
        self.brick_sprites = brick_sprites

    def __str__(self):
        return f"BallSprite({self.rect}, d={self.dy, self.dy})"

    def paddle_bounce(self, hit_paddle):
        sounds.bounce_sound.play()
        # This is how I want the ball to respond to hitting the paddle.
        # When the ball hits the paddle, its dy should become negative, so it goes up.
        self.dy = -abs(self.dy)
        # When the ball hits the middle part of the paddle, it should continue its current direction.
        # When the ball hits the left part of the paddle, it should go left, regardless of its current direction.
        # When the ball hits the right part of the paddle, it should go right, regardless of its current direction.
        # How do I know which part of the paddle was hit?
        # I can divide the paddle into 3 parts, and check which part the ball hit.
        num_parts = 3
        paddle_parts = [
            self.paddle_sprite.rect.x + i * self.paddle_sprite.width // num_parts
            for i in range(num_parts)
        ]
        # Check for left part of paddle.
        if paddle_parts[0] <= (self.rect.x + self.width * signum(self.dx)) < paddle_parts[1]:
            # print("Hit left", end=" ")
            self.dx = -abs(self.dx)
        elif paddle_parts[1] <= (self.rect.x + self.width * signum(self.dx)) < paddle_parts[2]:
            # print("Hit middle", end=" ")
            pass
        elif paddle_parts[2] <= (self.rect.x + self.width * signum(self.dx)) < self.paddle_sprite.rect.right:
            # print("Hit right", end=" ")
            self.dx = abs(self.dx)
        # print(f"paddle_parts={paddle_parts}", end=" ")
        # Calculate the new direction of the ball based on which side of the paddle was hit.
        # print(f"dx={self.dx}", end=" ")
        # change_bg_image()

    def brick_bounce(self, hit_brick):
        sounds.brick_sound.play()
        # Figure out which brick(s) were hit, so we can score appropriately.
        for brick in hit_brick:
            layer = (brick.rect.y - ABOVE_BRICKS) // BRICK_HEIGHT
            # add score based on layer
            self.glob.score.increment(BRICK_LAYER_COUNT - layer)
        # print(f"Score={self.glob.score}", end=" ")
    # Calculate the new direction of the ball based on which side of the brick was hit.
        if len(hit_brick) == 1:
            brick = hit_brick[0]
            # If hit the bottom or top of the brick, reverse dy and keep dx.
            # If hit the left or right of the brick, reverse dx and keep dy.
            # If hit the corner of the brick, reverse both dx and dy.
            print(f"Ball: {self}, Brick: {brick.rect}")
            if self.dy < 0 and brick.rect.top <= self.rect.top < brick.rect.bottom: # hit the bottom of a brick, reverse dy and keep dx.
                print("Hit bottom")
                self.dy = -self.dy
            elif self.dy > 0 and brick.rect.top <= self.rect.bottom < brick.rect.bottom: # hit the top of a brick, reverse dy and keep dx.
                print("Hit top")
                self.dy = -self.dy
            if self.dx < 0 and self.rect.left <= brick.rect.right < self.rect.right: # hit the right of a brick, reverse dx and keep dy.
                print("Hit right")
                self.dx = -self.dx
            elif self.dx > 0 and self.rect.left <= brick.rect.left < self.rect.right: # hit the left of a brick, reverse dx and keep dy.
                print("Hit left")
                self.dx = -self.dx
            return
        for brick in hit_brick:
            if self.rect.x < brick.rect.x:
                self.dx = abs(self.dx)
            if self.rect.x > brick.rect.x + brick.width:
                self.dx = -abs(self.dx)
            if self.rect.y < brick.rect.y:
                self.dy = abs(self.dy)
            if self.rect.y > brick.rect.y + brick.height:
                self.dy = -abs(self.dy)

    def update(self, events=None):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Check for paddle collision.
        hit_paddle = not DEMO and pygame.sprite.collide_rect(self.paddle_sprite, self)
        if hit_paddle:
            self.paddle_bounce(hit_paddle)
            return
        # Check for brick collision.
        hit_brick = pygame.sprite.spritecollide(
            self, self.brick_sprites, True
        )
        if hit_brick:  # Use elif because can't collide with both paddle and brick at the same time.
            self.brick_bounce(hit_brick)
            return

        # Normal bouncing off walls.
        # If the ball hits the bottom, the turn is over.
        if self.rect.y + self.radius > SCREEN_HEIGHT and not DEMO:
            sounds.bottom_sound.play()
            self.glob.pause = "bottom"
            return
        # If the ball has NOT hit the left, right or top walls, return.
        if not (self.rect.x + self.radius > RIGHT_MARGIN
            or self.rect.x <= LEFT_MARGIN
            or self.rect.y < 0
            or self.rect.y + self.radius > SCREEN_HEIGHT and DEMO
        ):
            return
        # Otherwise, make a sound and bounce off the wall.
        sounds.bounce_sound.play()
        if self.rect.x + self.radius > RIGHT_MARGIN or self.rect.x <= LEFT_MARGIN:
            if self.rect.x + self.radius > RIGHT_MARGIN:
                self.rect.x = RIGHT_MARGIN - self.radius
            if self.rect.x <= LEFT_MARGIN:
                self.rect.x = LEFT_MARGIN + 1
            self.dx = -self.dx
        if self.rect.y < 0 or (DEMO and self.rect.y + self.radius > SCREEN_HEIGHT):
            self.rect.y -= self.dy
            self.dy = -self.dy



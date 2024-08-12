# https://www.geeksforgeeks.org/pygame-creating-sprites/
# Object class
import pygame
from random import seed
from ball_sprite import BallSprite
from paddle_sprite import PaddleSprite
from brick_sprite import BrickSprite
from named_colors import named_colors
from score import Score
import sounds
from change_bg_image import change_bg_image
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT
    , LEFT_MARGIN, RIGHT_MARGIN, MARGIN_COLOR
    , BRICKS_X_COUNT, BRICK_LAYER_COUNT
    , BELOW_PADDLE
    , BALL_RADIUS
    , DEMO)
from dataclasses import dataclass


def is_quit(event) -> bool:
    return (
        event.type == pygame.QUIT
        or event.type == pygame.KEYDOWN
        and event.key == pygame.K_ESCAPE
        or event.type == pygame.KEYDOWN
        and event.key == pygame.K_q
    )


SURFACE_IMAGE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


pygame.init()
seed(__file__)

RED = pygame.Color("red")

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creating Sprites Tutorial")
score_font = pygame.freetype.SysFont("Comic Sans", 30)

paddle_sprite = PaddleSprite()
paddle_sprite.rect.x = (SCREEN_WIDTH - paddle_sprite.width) // 2
paddle_sprite.rect.y = SCREEN_HEIGHT - paddle_sprite.height - BELOW_PADDLE

# The bricks are in a list so we can do collision detection.
brick_list = [
    BrickSprite(x, y) for x in range(BRICKS_X_COUNT) for y in range(BRICK_LAYER_COUNT)
]
brick_sprites = pygame.sprite.Group(brick_list)


@dataclass
class Glob():
    game_speed: int
    pause: str
    score: Score
    def __init__(self):
        self.game_speed = 10
        self.pause = ""
        self.score = Score()

glob = Glob()


ball_sprite = BallSprite(named_colors["white"], BALL_RADIUS, glob, paddle_sprite, brick_sprites)
ball_sprite.rect.x = 200
ball_sprite.rect.y = 300

all_sprites = pygame.sprite.Group()
all_sprites.add(ball_sprite)
all_sprites.add(paddle_sprite)


sounds.initialize_sounds()


def redraw(screen):
    screen.blit(SURFACE_IMAGE, (0, 0))
    for margin in (LEFT_MARGIN, RIGHT_MARGIN):
        pygame.draw.line(screen, MARGIN_COLOR, (margin, 0), (margin, SCREEN_HEIGHT))
    all_sprites.draw(screen)
    brick_sprites.draw(screen)
    # Show score in pygame window:
    score_surface, score_rect = score_font.render(f"{glob.score}", named_colors["white"])
    screen.blit(score_surface, (RIGHT_MARGIN - score_rect.width - 10, 10))
    # Indicate if in demo mode.
    if DEMO:
        demo_surface, demo_rect = score_font.render("DEMO", named_colors["white"])
        screen.blit(demo_surface, (LEFT_MARGIN + 10, 10))
    else:
        demo_surface, demo_rect = score_font.render("OUTBREAK!", named_colors["white"])
        screen.blit(demo_surface, (LEFT_MARGIN + 10, 10))
    pygame.display.flip()


def run_game():
    running = True
    glob.pause = ""  # Pause the game when the ball hits bottom.
    glob.game_speed = 10
    clock = pygame.time.Clock()

    # print(all_sprites.sprites())

    while running:
        clock.tick(glob.game_speed)
        events = pygame.event.get()
        for event in events:
            if is_quit(event):
                running = False
                break
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_b:
                        change_bg_image()
                    case pygame.K_p:
                        glob.pause = not glob.pause
                        print("Pause:", glob.pause)
                    case pygame.K_f:
                        glob.game_speed += 10
                    case pygame.K_s:
                        glob.game_speed -= 10
                        if glob.game_speed < 1:
                            glob.game_speed = 1
        # Check for key presses
        keys = pygame.key.get_pressed()
        if not glob.pause:
            paddle_sprite.handle_event(keys)
            # Update sprites
            all_sprites.update(events)

        # Repaint the screen
        redraw(screen)


if __name__ == "__main__":
    run_game()
    pygame.quit()

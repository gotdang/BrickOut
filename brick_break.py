# https://www.geeksforgeeks.org/pygame-creating-sprites/
from pathlib import Path
import pygame
import pygame.freetype
from random import choice, Random, seed
from signum import signum
from named_colors import named_colors

if True:  # force window to upper left corner during development.
    import os
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"

# Globals
COLOR = 255, 100, 98
SURFACE_COLOR = named_colors["grayf"]  # 167, 255, 100
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

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BELOW_PADDLE = 1 * PADDLE_HEIGHT
DEMO = False

# Object class
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()


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


class BallSprite(GameSprite):
    x_speeds = (5, 10, 15)
    y_speeds = (2, 3, 4)

    def __init__(self, color, radius):
        super().__init__(color, radius, radius)
        self.radius = radius
        self.dx = choice((-1, 1)) * self.x_speeds[len(self.x_speeds) // 2]
        self.dy = self.y_speeds[len(self.y_speeds) // 2]

    def __str__(self):
        return f"BallSprite({self.rect}, d={self.dy, self.dy})"

    def paddle_bounce(self, hit_paddle):
        bounce_sound.play()
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
            paddle_sprite.rect.x + i * paddle_sprite.width // num_parts
            for i in range(num_parts)
        ]
        # Check for left part of paddle.
        if paddle_parts[0] <= (self.rect.x + self.width * signum(self.dx)) < paddle_parts[1]:
            # print("Hit left", end=" ")
            self.dx = -abs(self.dx)
        elif paddle_parts[1] <= (self.rect.x + self.width * signum(self.dx)) < paddle_parts[2]:
            # print("Hit middle", end=" ")
            pass
        elif paddle_parts[2] <= (self.rect.x + self.width * signum(self.dx)) < paddle_sprite.rect.right:
            # print("Hit right", end=" ")
            self.dx = abs(self.dx)
        # print(f"paddle_parts={paddle_parts}", end=" ")
        # Calculate the new direction of the ball based on which side of the paddle was hit.
        # print(f"dx={self.dx}", end=" ")
        # change_bg_image()

    def brick_bounce(self, hit_brick):
        global score
        brick_sound.play()
        # Figure out which brick(s) were hit, so we can score appropriately.
        for brick in hit_brick:
            layer = (brick.rect.y - ABOVE_BRICKS) // BRICK_HEIGHT
            # add score based on layer
            score += BRICK_LAYER_COUNT - layer
        # print(f"Score={score}", end=" ")
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
        global pause
        global score
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Check for paddle collision.
        hit_paddle = not DEMO and pygame.sprite.collide_rect(paddle_sprite, ball_sprite)
        if hit_paddle:
            self.paddle_bounce(hit_paddle)
            return
        # Check for brick collision.
        hit_brick = pygame.sprite.spritecollide(
            ball_sprite, brick_sprites, True
        )
        if hit_brick:  # Use elif because can't collide with both paddle and brick at the same time.
            self.brick_bounce(hit_brick)
            return

        # Normal bouncing off walls.
        # If the ball hits the bottom, the turn is over.
        if self.rect.y + self.radius > SCREEN_HEIGHT and not DEMO:
            bottom_sound.play()
            pause = "bottom"
            return
        # If the ball has NOT hit the left, right or top walls, return.
        if not (self.rect.x + self.radius > RIGHT_MARGIN
            or self.rect.x <= LEFT_MARGIN
            or self.rect.y < 0
            or self.rect.y + self.radius > SCREEN_HEIGHT and DEMO
        ):
            return
        # Otherwise, make a sound and bounce off the wall.
        bounce_sound.play()
        if self.rect.x + self.radius > RIGHT_MARGIN or self.rect.x <= LEFT_MARGIN:
            if self.rect.x + self.radius > RIGHT_MARGIN:
                self.rect.x = RIGHT_MARGIN - self.radius
            if self.rect.x <= LEFT_MARGIN:
                self.rect.x = LEFT_MARGIN + 1
            self.dx = -self.dx
        if self.rect.y < 0 or (DEMO and self.rect.y + self.radius > SCREEN_HEIGHT):
            self.rect.y -= self.dy
            self.dy = -self.dy


class PaddleSprite(GameSprite):
    def __init__(self, color, width, height):
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


class ClickableSprite(GameSprite):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.visible = True

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    self.on_click(event)

    def on_click(self, event):
        # click_sound.play()
        self.visible = not self.visible
        change_bg_image()
        if self.visible:
            print("Visible.", end=" ")
        else:
            print("Not visible.", end=" ")

    def draw(self, screen):
        print("BORK!", end=" ")
        if self.visible:
            screen.blit(self.image, self.rect)
            print("Drawing clickable sprite.", end=" ")
        else:
            print("Not drawing clickable sprite.", end=" ")


def is_quit(event) -> bool:
    return (
        event.type == pygame.QUIT
        or event.type == pygame.KEYDOWN
        and event.key == pygame.K_ESCAPE
        or event.type == pygame.KEYDOWN
        and event.key == pygame.K_q
    )


SURFACE_IMAGE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


def change_bg_image():
    global SURFACE_IMAGE
    surface_image = bg_rng.choice(BG_IMAGES)
    SURFACE_IMAGE = pygame.image.load(surface_image).convert()
    SURFACE_IMAGE = pygame.transform.scale(SURFACE_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print(surface_image)


pygame.init()
seed(__file__)
bg_rng = Random()

RED = pygame.Color("red")

score = 0

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creating Sprites Tutorial")
score_font = pygame.freetype.SysFont("Comic Sans", 30)

all_sprites = pygame.sprite.Group()

ball_sprite = BallSprite(named_colors["white"], BALL_RADIUS)
ball_sprite.rect.x = 200
ball_sprite.rect.y = 300

paddle_sprite = PaddleSprite(RED, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_sprite.rect.x = (SCREEN_WIDTH - paddle_sprite.width) // 2
paddle_sprite.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - BELOW_PADDLE

# click_sprite = ClickableSprite(pygame.Color("gray7"), 100, 100)

all_sprites.add(ball_sprite)
all_sprites.add(paddle_sprite)
# all_sprites.add(click_sprite)

# The bricks are in a list so we can do collision detection.
brick_list = [
    BrickSprite(x, y) for x in range(BRICKS_X_COUNT) for y in range(BRICK_LAYER_COUNT)
]
brick_sprites = pygame.sprite.Group(brick_list)

bounce_sound = None
brick_sound = None
bottom_sound = None
def initialize_sounds():
    global bottom_sound, bounce_sound, brick_sound
    sound_dir = Path(Path(__file__).parent, "audio")
    # https://freesound.org/people/deathbyfairydust/sounds/658431/
    bounce_sound = pygame.mixer.Sound(
        Path(sound_dir, "658431__deathbyfairydust__pop.wav")
    )
    # https://freesound.org/people/LittleRobotSoundFactory/sounds/288951/
    # brick_sound = pygame.mixer.Sound(Path(sound_dir, "288951__littlerobotsoundfactory__click_electronic_01.wav"))
    brick_sound = pygame.mixer.Sound(
        Path(sound_dir, "290420__littlerobotsoundfactory__mouth_05.wav")
    )
    # brick_sound = pygame.mixer.Sound(Path(sound_dir, "506546__matrixxx__pop-01.wav"))
    # brick_sound = pygame.mixer.Sound(Path(sound_dir, "506545__matrixxx__pop-02.wav"))
    # print(f"Sound volume: {bounce_sound.get_volume()}")
    bottom_sound = pygame.mixer.Sound(
        Path(sound_dir, "483598__raclure__wrong.mp3")
    )
    for sound in (bounce_sound, brick_sound):
        # sound.set_volume(0.0625)
        sound.set_volume(0.125)
        # print(f"Sound volume: {sound.get_volume()}")


def redraw(screen):
    screen.blit(SURFACE_IMAGE, (0, 0))
    for margin in (LEFT_MARGIN, RIGHT_MARGIN):
        pygame.draw.line(screen, MARGIN_COLOR, (margin, 0), (margin, SCREEN_HEIGHT))
    all_sprites.draw(screen)
    brick_sprites.draw(screen)
    # Show score in pygame window:
    score_surface, score_rect = score_font.render(f"{score}", named_colors["white"])
    screen.blit(score_surface, (RIGHT_MARGIN - score_rect.width - 10, 10))
    # Indicate if in demo mode.
    if DEMO:
        demo_surface, demo_rect = score_font.render("DEMO", named_colors["white"])
        screen.blit(demo_surface, (LEFT_MARGIN + 10, 10))
    else:
        demo_surface, demo_rect = score_font.render("OUTBREAK!", named_colors["white"])
        screen.blit(demo_surface, (LEFT_MARGIN + 10, 10))
    pygame.display.flip()


initialize_sounds()


def run_game():
    global pause
    running = True
    pause = ""  # Pause the game when the ball hits bottom.
    game_speed = 10
    clock = pygame.time.Clock()

    # print(all_sprites.sprites())

    while running:
        clock.tick(game_speed)
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
                        pause = not pause
                        print("Pause:", pause)
                    case pygame.K_f:
                        game_speed += 10
                    case pygame.K_s:
                        game_speed -= 10
                        if game_speed < 1:
                            game_speed = 1
        # Check for key presses
        keys = pygame.key.get_pressed()
        if not pause:
            paddle_sprite.handle_event(keys)
            # Update sprites
            all_sprites.update(events)

        # Repaint the screen
        redraw(screen)


run_game()
pygame.quit()

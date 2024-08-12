import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BG_IMAGES
from random import Random


bg_rng = Random()


def change_bg_image():
    global SURFACE_IMAGE
    surface_image = bg_rng.choice(BG_IMAGES)
    SURFACE_IMAGE = pygame.image.load(surface_image).convert()
    SURFACE_IMAGE = pygame.transform.scale(SURFACE_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print(surface_image)



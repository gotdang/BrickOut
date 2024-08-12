from pathlib import Path
import pygame


bounce_sound = None
brick_sound = None
bottom_sound = None
hi_beep_sound = None


def initialize_sounds():
    global bottom_sound, bounce_sound, brick_sound, hi_beep_sound
    sound_dir = Path(Path(__file__).parent, "audio")
    bounce_sound = pygame.mixer.Sound(Path(sound_dir, "658431__deathbyfairydust__pop.wav"))
    brick_sound = pygame.mixer.Sound(Path(sound_dir, "290420__littlerobotsoundfactory__mouth_05.wav"))
    bottom_sound = pygame.mixer.Sound(Path(sound_dir, "483598__raclure__wrong.mp3"))
    hi_beep_sound = pygame.mixer.Sound(Path(sound_dir, "350865__cabled_mess__blip_c_01.wav"))
    for sound in (bounce_sound, brick_sound):
        # sound.set_volume(0.0625)
        sound.set_volume(0.125)
        # print(f"Sound volume: {sound.get_volume()}")

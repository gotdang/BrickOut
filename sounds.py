from pathlib import Path
import pygame


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

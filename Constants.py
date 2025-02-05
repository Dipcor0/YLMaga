import pygame
from pygame import mixer
import os
import sys

mixer.init()

# SIZE
SIZE_SCREEN = (1920, 1080)
SIZE_ZONE_STORE = 450, 450

# COLOR
COLOR_SCREEN = pygame.Color('pink')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# OTHER
MONEY = 0
CRISTALLS = 0

# PLAYER
PLAYER_LEVEL = 1
PLAYER_HP = 100
PLAYER_SPEED_MOVE = 5  # я затестил 52 чето не то, поэтому лучше 5
PLAYER_ARMOR = 50
PLAYER_WEAPON = [0]  # индекс
PLAYER_EQUIPMENT = [0]  # индексы(база индексов лежит в функции Equipment.get_equipment

# Для инвентаря
UI_HEIGHT = 200
SCREEN_WIDTH_BATTLE, SCREEN_HEIGHT_BATTLE = pygame.display.set_mode((0, 0), pygame.FULLSCREEN).get_size()
FIELD_WIDTH = SCREEN_WIDTH_BATTLE
FIELD_HEIGHT = SCREEN_HEIGHT_BATTLE - UI_HEIGHT
SLOT_SIZE = 50
WIDTH, HEIGHT = 800, 600
FPS = 60
INVENTORY_SLOTS = 5  # Количество ячеек в инвентаре
# для мобов буду свои значения

# Sptites
PLAYER_IMAGE = None
BACKGROUND_IMAGE = None
HEART_IMAGE = None
ARMOR_IMAGE = None
CRYSTAL_IMAGE = None
COIN_IMAGE = None
MOB_IMAGE = None
BACKGROUND_MARKET_IMAGE = None
TELEPORT_FIGHT = None
TELEPORT_FIGHT_ACTIVE = None

def download_save():
    #  будем использовать базу данных SQL
    pass


# Music/Sound
WELM_SCREAM = mixer.Sound("Music/Wilhelm4.ogg")
FIREBALL_SPAWN_SOUND = mixer.Sound("Music/fireball_cast.ogg")
NEEDLE_SWISH_SOUND = mixer.Sound("Music/needle_cast.ogg")
CORONA_VIRUS = mixer.Sound("Music/corona_virus.ogg")

def load_sprites():
    global PLAYER_IMAGE, BACKGROUND_IMAGE, HEART_IMAGE, \
        ARMOR_IMAGE, CRYSTAL_IMAGE, COIN_IMAGE, MOB_IMAGE, BACKGROUND_MARKET_IMAGE, TELEPORT_FIGHT, TELEPORT_FIGHT_ACTIVE

    def load_image(road, name, ):
        fullname = os.path.join(road, name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        return image

    PLAYER_IMAGE = load_image('Sprites/Creatures', 'персонаж.png')
    BACKGROUND_IMAGE = load_image('Sprites/Creatures', 'полеБоя.png')
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (FIELD_WIDTH, FIELD_HEIGHT))
    HEART_IMAGE = load_image('Sprites/Creatures', 'сердце.png')
    HEART_IMAGE = pygame.transform.scale(HEART_IMAGE, (30, 30))

    ARMOR_IMAGE = load_image('Sprites/Creatures', 'броня.png')
    ARMOR_IMAGE = pygame.transform.scale(ARMOR_IMAGE, (30, 30))

    BOAR_IMAGE = load_image('Sprites/Creatures', 'boar.png')
    BOAR_IMAGE = pygame.transform.scale(BOAR_IMAGE, (70, 70))

    CRYSTAL_IMAGE = load_image('Sprites/Creatures', 'кристалик.png')
    CRYSTAL_IMAGE = pygame.transform.scale(CRYSTAL_IMAGE, (30, 30))
    COIN_IMAGE = load_image('Sprites/Creatures', 'монетка.png')
    COIN_IMAGE = pygame.transform.scale(COIN_IMAGE, (30, 30))
    MOB_IMAGE = load_image('Sprites/Creatures', 'моб.png')
    MOB_IMAGE = pygame.transform.scale(MOB_IMAGE, (60, 60))
    BACKGROUND_MARKET_IMAGE = load_image('Sprites/Creatures', 'ЗаднийФонМагазина.png')

    TELEPORT_FIGHT = load_image('Sprites/Creatures', 'тп.png')
    TELEPORT_FIGHT = pygame.transform.scale(TELEPORT_FIGHT, (TELEPORT_FIGHT.get_width() * 3.5,
                                                             TELEPORT_FIGHT.get_height() * 3.5))
    TELEPORT_FIGHT_ACTIVE = load_image('Sprites/Creatures', 'тп актив.png')
    TELEPORT_FIGHT_ACTIVE = pygame.transform.scale(TELEPORT_FIGHT_ACTIVE, (TELEPORT_FIGHT_ACTIVE.get_width() * 3.5,
                                                             TELEPORT_FIGHT_ACTIVE.get_height() * 3.5))



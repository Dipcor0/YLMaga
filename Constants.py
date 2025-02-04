import pygame
import os
import sys

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
PLAYER_WEAPON = [0, 1, 2]  # индекс
PLAYER_EQUIPMENT = []  # индексы(база индексов лежит в функции Equipment.get_equipment

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


def download_save():
    #  будем использовать базу данных SQL
    pass


def upload_save():
    #  будем использовать базу данных SQL
    pass


def load_sprites():
    global PLAYER_IMAGE, BACKGROUND_IMAGE, HEART_IMAGE, \
        ARMOR_IMAGE, CRYSTAL_IMAGE, COIN_IMAGE, MOB_IMAGE, BACKGROUND_MARKET_IMAGE

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

    CRYSTAL_IMAGE = load_image('Sprites/Creatures', 'кристалик.png')
    CRYSTAL_IMAGE = pygame.transform.scale(CRYSTAL_IMAGE, (30, 30))
    COIN_IMAGE = load_image('Sprites/Creatures', 'монетка.png')
    COIN_IMAGE = pygame.transform.scale(COIN_IMAGE, (30, 30))
    MOB_IMAGE = load_image('Sprites/Creatures', 'моб.png')
    MOB_IMAGE = pygame.transform.scale(MOB_IMAGE, (60, 60))
    BACKGROUND_MARKET_IMAGE = load_image('Sprites/Creatures', 'ЗаднийФонМагазина.png')

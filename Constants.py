import pygame
import os
import sys

# SIZE
SIZE_SCREEN = 1920, 1000
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

# INFO ABOUT CREATURES
GROUP_PLAYER = pygame.sprite.Group()
# PLAYER
PLAYER_LEVEL = 1
PLAYER_HP = 100
PLAYER_REGEN = 1  # * t
PLAYER_HIT = 10
PLAYER_SPEED_MOVE = 5 # я затестил 52 чето не то, поэтому лучше 5
PLAYER_CHANCE_CRIT = 0.1
PLAYER_KOEF_CRIT = 1
PLAYER_ARMOR = 50
PLAYER_CHANCE_AVOIDANCE = 0.1
PLAYER_WEAPON = 0  # сделаем базу данных из оружий
PLAYER_IMAGE = None

# Для инвентаря
SLOT_SIZE = 50
WIDTH, HEIGHT = 800, 600
FPS = 60
INVENTORY_SLOTS = 5  # Количество ячеек в инвентаре
UI_HEIGHT = 200
# для мобов буду свои значения


def download_save():
    #  будем использовать базу данных SQL
    pass


def upload_save():
    #  будем использовать базу данных SQL
    pass


def load_sprites():
    global PLAYER_IMAGE

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

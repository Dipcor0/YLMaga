import pygame

# SIZE
SIZE_SCREEN = 1920, 1000

# COLOR
COLOR_SCREEN = pygame.Color('pink')

# OTHER
active_scene = 1

# INFO ABOUT CREATURES
# PLAYER
PLAYER_LEVEL = 1
PLAYER_HP = 100
PLAYER_REGEN = 1  # * t
PLAYER_HIT = 10
PLAYER_SPEED_MOVE = 52
PLAYER_CHANCE_CRIT = 0.1
PLAYER_KOEF_CRIT = 1
PLAYER_ARMOR = 50
PLAYER_CHANCE_AVOIDANCE = 0.1
PLAYER_WEAPON = 0  # сделаем базу данных из оружий


# для мобов буду свои значения


def download_save():
    #  будем использовать базу данных SQL
    pass


def upload_save():
    #  будем использовать базу данных SQL
    pass

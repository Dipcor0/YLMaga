import pygame
from pygame import mixer
import os
import sys
import csv

mixer.init()
# SIZE
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SIZE_SCREEN = screen.get_size()
SIZE_ZONE_STORE = 450, 450
SIZE_BOX = (180, 300)

# COLOR
COLOR_SCREEN = pygame.Color('pink')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (108, 207, 227)
DARK_BLUE = (10, 110, 130)
DARK_DARK_BLUE = (0, 53, 64)
LIGHT_BLUE = (5, 209, 250)
GRAY = (100, 100, 100)

# OTHER
MONEY = 0
CRYSTALS = 0

# PLAYER
PLAYER_LEVEL = 1
PLAYER_HP = 100
PLAYER_SPEED_MOVE = 5  # я затестил 52 чето не то, поэтому лучше 5
PLAYER_ARMOR = 50
PLAYER_WEAPON = []  # индекс
PLAYER_EQUIPMENT = []  # индексы(база индексов лежит в функции Equipment.get_equipment

ALL_WEAPON = []
ALL_EQUIPMENT = []

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
UPGRADE_MAGIC_BALL_IMAGE = None
UPGRADE_MAGIC_HANDS_IMAGE = None
NEEDLE_IMAGE = None
FIREBALL_IMAGE = None
BOAR_IMAGE = None
SHOP_IMAGE = None


def download_save():
    global MONEY, CRYSTALS, PLAYER_LEVEL, ALL_EQUIPMENT, ALL_WEAPON, PLAYER_EQUIPMENT, PLAYER_WEAPON
    with open('save.csv', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        res = list(reader)[0]
        PLAYER_LEVEL = int(res['PLAYER_LVL'])
        MONEY = int(res['MONEY'])
        CRYSTALS = int(res['CRYSTALS'])
        if res['ALL_WEAP'] != '':
            ALL_WEAPON = list(map(int, res['ALL_WEAP'].split(','))).copy()
        if res['ALL_EQ'] != '':
            ALL_EQUIPMENT = list(map(int, res['ALL_EQ'].split(','))).copy()

        if res['ACT_EQ'] != '':
            PLAYER_EQUIPMENT = list(map(int, res['ACT_EQ'].split(','))).copy()
        if res['ACT_WEAP'] != '':
            PLAYER_WEAPON = list(map(int, res['ACT_WEAP'].split(','))).copy()


def save():
    global MONEY, CRYSTALS, PLAYER_LEVEL, ALL_EQUIPMENT, ALL_WEAPON, PLAYER_EQUIPMENT, PLAYER_WEAPON
    data = {'PLAYER_LVL': PLAYER_LEVEL, 'MONEY': MONEY, 'CRYSTALS': CRYSTALS,
            'ALL_WEAP': ','.join(map(str, ALL_WEAPON)),
            'ALL_EQ': ','.join(map(str, ALL_EQUIPMENT)),
            'ACT_EQ': ','.join(map(str, PLAYER_EQUIPMENT)),
            'ACT_WEAP': ','.join(map(str, PLAYER_WEAPON))}
    with open('save.csv', 'w', encoding="utf8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()), delimiter=';')
        writer.writeheader()
        writer.writerow(data)


# Music/Sound
WELM_SCREAM = mixer.Sound("Music/Wilhelm4.ogg")
FIREBALL_SPAWN_SOUND = mixer.Sound("Music/fireball_cast.ogg")
NEEDLE_SWISH_SOUND = mixer.Sound("Music/needle_cast.ogg")
CORONA_VIRUS = mixer.Sound("Music/coronavirus.ogg")


def load_image(road, name):
    fullname = os.path.join(road, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


def load_sprites():
    global PLAYER_IMAGE, BACKGROUND_IMAGE, HEART_IMAGE, \
        ARMOR_IMAGE, CRYSTAL_IMAGE, COIN_IMAGE, MOB_IMAGE, \
        BACKGROUND_MARKET_IMAGE, TELEPORT_FIGHT, TELEPORT_FIGHT_ACTIVE, \
        UPGRADE_MAGIC_BALL_IMAGE, UPGRADE_MAGIC_HANDS_IMAGE, FIREBALL_IMAGE, NEEDLE_IMAGE, BOAR_IMAGE, SHOP_IMAGE

    PLAYER_IMAGE = load_image('Sprites/Creatures', 'персонаж.png')
    BACKGROUND_IMAGE = load_image('Sprites/Structures', 'полеБоя.png')
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (FIELD_WIDTH, FIELD_HEIGHT))
    HEART_IMAGE = load_image('Sprites/Other', 'сердце.png')
    HEART_IMAGE = pygame.transform.scale(HEART_IMAGE, (30, 30))

    ARMOR_IMAGE = load_image('Sprites/Equipments', 'броня.png')
    ARMOR_IMAGE = pygame.transform.scale(ARMOR_IMAGE, (30, 30))

    BOAR_IMAGE = load_image('Sprites/Creatures', 'boar.png')
    BOAR_IMAGE = pygame.transform.scale(BOAR_IMAGE, (70, 70))

    CRYSTAL_IMAGE = load_image('Sprites/Other', 'кристалик.png')
    CRYSTAL_IMAGE = pygame.transform.scale(CRYSTAL_IMAGE, (30, 30))
    COIN_IMAGE = load_image('Sprites/Other', 'монетка.png')
    COIN_IMAGE = pygame.transform.scale(COIN_IMAGE, (30, 30))
    MOB_IMAGE = load_image('Sprites/Creatures', 'моб.png')
    MOB_IMAGE = pygame.transform.scale(MOB_IMAGE, (60, 60))
    BACKGROUND_MARKET_IMAGE = load_image('Sprites/Structures', 'ЗаднийФонМагазина.png')

    TELEPORT_FIGHT = load_image('Sprites/Structures', 'тп.png')
    TELEPORT_FIGHT = pygame.transform.scale(TELEPORT_FIGHT, (TELEPORT_FIGHT.get_width() * 3.5,
                                                             TELEPORT_FIGHT.get_height() * 3.5))
    TELEPORT_FIGHT_ACTIVE = load_image('Sprites/Structures', 'тп актив.png')
    TELEPORT_FIGHT_ACTIVE = pygame.transform.scale(TELEPORT_FIGHT_ACTIVE, (TELEPORT_FIGHT_ACTIVE.get_width() * 3.5,
                                                                           TELEPORT_FIGHT_ACTIVE.get_height() * 3.5))

    UPGRADE_MAGIC_BALL_IMAGE = load_image('Sprites/Structures', 'магический шар2.png')
    UPGRADE_MAGIC_BALL_IMAGE = pygame.transform.scale(UPGRADE_MAGIC_BALL_IMAGE,
                                                      (UPGRADE_MAGIC_BALL_IMAGE.get_width() * 1.5,
                                                       UPGRADE_MAGIC_BALL_IMAGE.get_height() * 1.5))

    UPGRADE_MAGIC_HANDS_IMAGE = load_image('Sprites/Structures', 'руки мш.png')
    UPGRADE_MAGIC_HANDS_IMAGE = pygame.transform.scale(UPGRADE_MAGIC_HANDS_IMAGE,
                                                       (UPGRADE_MAGIC_HANDS_IMAGE.get_width() * 1.5,
                                                        UPGRADE_MAGIC_HANDS_IMAGE.get_height() * 1.5))

    SHOP_IMAGE = load_image('Sprites/Structures', 'shop_beta.png')

import pygame
import Constants
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, PLAYER_HP, PLAYER_ARMOR, RED, WHITE, SLOT_SIZE, INVENTORY_SLOTS, \
    FIELD_HEIGHT, FIELD_WIDTH, FPS, GRAY


class Creature(pygame.sprite.Sprite):
    def __init__(self, group, image, pos):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, event=None, tick=None):
        pass

    def draw(self, screen):
        pass


class Boss(Creature):
    def __init__(self, group, image, pos):
        super().__init__(group, image, pos)


# пример противника
class Enemy(Creature):
    def __init__(self, group, image, pos):
        super().__init__(group, image, pos)
        self.money = 52
        self.exp = 52
        self.hp = 1000

    def get_damage(self, hit: int):
        self.hp -= hit
        if self.hp <= 0:
            self.kill()

    def kill(self):
        # что-то, чтобы противник изчез с поля
        return self.money, self.exp


# class Hero(Creature):
#     def __init__(self):
#         super().__init__(Constants.GROUP_PLAYER, Constants.PLAYER_IMAGE, (0, 0))
#         self.speed = Constants.PLAYER_SPEED_MOVE
#         self.can_move = True
#         self.rect.x = 500  # куча данных персонажа. От сюда
#         self.rect.y = 500
#         self.level = Constants.PLAYER_LEVEL
#         self.hp = Constants.PLAYER_HP
#         self.regen = Constants.PLAYER_REGEN
#         self.hit = Constants.PLAYER_HIT
#         self.chane_crit = Constants.PLAYER_CHANCE_CRIT
#         self.koef_krit = Constants.PLAYER_KOEF_CRIT
#         self.armor = Constants.PLAYER_ARMOR
#         self.chance_avoidence = Constants.PLAYER_CHANCE_AVOIDANCE  # До сюда
#         self.inventory = []
#         self.armor_sprite = None  # Добавляем атрибут для брони
#
#     def update(self, event=None, tick=None):
#         if self.can_move:
#             keys = pygame.key.get_pressed()
#             if keys[pygame.K_w] and self.rect.top > 0:
#                 self.rect.y -= self.speed
#             if keys[pygame.K_s] and self.rect.bottom < Constants.SIZE_SCREEN[1]:
#                 self.rect.y += self.speed
#             if keys[pygame.K_a] and self.rect.left > 0:
#                 self.rect.x -= self.speed
#             if keys[pygame.K_d] and self.rect.right < Constants.SIZE_SCREEN[0]:
#                 self.rect.x += self.speed
#
#     def move(self, dx, dy):  # изменение координаты во время движения
#         self.rect = self.rect.move(dx, dy)
#
#     def get_coords(self):
#         return [self.rect.x, self.rect.y]
#
#     def get_hp(self):
#         return self.hp
#
#     def get_armor(self):
#         return self.armor
#
#     def get_inventory(self):
#         return self.inventory
#
#     def block_move(self):
#         self.can_move = not self.can_move
#
#     def block_right(self):
#         pass
#
#     def block_left(self):
#         pass
#
#     def block_up(self):
#         pass
#
#     def block_down(self):
#         pass
#
#     def upgrade_characteristics(self, armor):
#         if armor:
#             armor.upgrade_armor(self)


'''
TODO: Сделать csv файл, в котором будут хранится данные о всех оружиях и снаряжении. 
В снаряжении будет колонка name - имя снаряжения, use_now - в инвентаре ли снаряга (значения 0/1), 
buff_type - тип улучшения (hp, armor, regen и тд), quantity - значение усиления (10, 20, 100, 250, 500)
TODO: В функцию upgrade_characteristics передавать список  из csv файла с именами снаряжения, 
сделать цикл проверки использования в инвентаре, определения типа улучшения, 
добавления добавочного значения к истинному
'''


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/Creatures/персонаж.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        self.speed = PLAYER_SPEED_MOVE

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < FIELD_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < FIELD_WIDTH:
            self.rect.x += self.speed

    def upgrade_characteristics(self, armor, boots):
        if armor:
            armor.upgrade_armor(self)
        if boots:
            boots.upgrade_armor(self)


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Constants.MOB_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.attack_cooldown = 1000  # 1 секунда
        self.last_attack_time = pygame.time.get_ticks()
        self.hp = 100  # Добавлено здоровье

    def can_attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = now
            return True
        return False

    def update(self, target):
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        if self.rect.x > target.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        if self.rect.y > target.rect.y:
            self.rect.y -= self.speed

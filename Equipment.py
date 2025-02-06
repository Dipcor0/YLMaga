import pygame
from pygame import mixer
import math
from Constants import FIELD_WIDTH, FIELD_HEIGHT, PLAYER_EQUIPMENT, FPS, WELM_SCREAM, FIREBALL_SPAWN_SOUND, CORONA_VIRUS, \
    NEEDLE_SWISH_SOUND

needle_image = pygame.image.load("Sprites/Creatures/needle_image.png").convert_alpha()
needle_image = pygame.transform.scale(needle_image, (30, 30))

fireball_image = pygame.image.load("Sprites/Creatures/фаербол.png").convert_alpha()
fireball_image = pygame.transform.scale(fireball_image, (30, 30))  # Загружаем изображение

mixer.init()


class Needles(pygame.sprite.Sprite):
    reload = FPS * 2 // 3
    image = needle_image
    speed = 15
    damage = 15
    name = 'Шипы'

    def __init__(self, group, pos_hero, enemies):
        super().__init__(group)
        #  self.image = self.image_wn  # Загруженное изображение иглы
        self.rect = self.image.get_rect(center=pos_hero)
        self.direction = self.get_direction(enemies)
        self.hit_targets = set()  # Запоминаем, кого уже поразили

        NEEDLE_SWISH_SOUND.play()

    def get_direction(self, enemies):
        if enemies:
            target = min(enemies, key=lambda enemy: math.hypot(self.rect.x - enemy.rect.x, self.rect.y - enemy.rect.y))
            dir_x = target.rect.x - self.rect.x
            dir_y = target.rect.y - self.rect.y
            length = math.hypot(dir_x, dir_y)
            if length != 0:
                return dir_x / length, dir_y / length
        return 1, 0  # Если врагов нет, летит вправо

    def update(self, enemies):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        for enemy in enemies.copy():
            if self.rect.colliderect(enemy.rect) and enemy not in self.hit_targets:
                enemy.hp -= self.damage  # Наносим урон
                self.hit_targets.add(enemy)  # Запоминаем, что уже нанесли урон
                if enemy.hp <= 0:
                    WELM_SCREAM.play()
                    enemy.kill()  # Удаляем моба после смерти

        # Удаляем иглу, если она выходит за границы экрана
        if (self.rect.right < 0 or self.rect.left > FIELD_WIDTH or
                self.rect.bottom < 0 or self.rect.top > FIELD_HEIGHT):
            self.kill()


class Fireball(pygame.sprite.Sprite):
    reload = FPS * 1.5
    speed = 7  # Скорость чуть меньше, чем у иглы
    damage = 50  # Урон
    image = fireball_image
    name = 'Фаербол'

    def __init__(self, group, pos_hero, enemies):
        super().__init__(group)
        self.rect = self.image.get_rect(center=pos_hero)
        self.direction = self.get_direction(enemies)

        FIREBALL_SPAWN_SOUND.play()

    def get_direction(self, enemies):
        if enemies:
            target = min(enemies, key=lambda enemy: math.hypot(self.rect.x - enemy.rect.x, self.rect.y - enemy.rect.y))
            dir_x = target.rect.x - self.rect.x
            dir_y = target.rect.y - self.rect.y
            length = math.hypot(dir_x, dir_y)
            if length != 0:
                return dir_x / length, dir_y / length
        return 1, 0  # Если врагов нет, летит вправо

    def update(self, enemies):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        for enemy in enemies.copy():
            if self.rect.colliderect(enemy.rect):
                enemy.hp -= self.damage  # Наносим урон
                if enemy.hp <= 0:
                    WELM_SCREAM.play()
                    enemy.kill()  # Удаляем моба после смерти
                self.kill()  # Удаляем фаербол после первого попадания
                return

        # Удаляем фаербол, если он выходит за границы экрана
        if (self.rect.right < 0 or self.rect.left > FIELD_WIDTH or
                self.rect.bottom < 0 or self.rect.top > FIELD_HEIGHT):
            self.kill()


class SocialDistance(pygame.sprite.Sprite):
    reload = FPS
    damage = 10
    radius = 100
    image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(image, (207, 76, 0) + (128,), (radius, radius),
                       radius)  # 128 - это уровень прозрачности
    name = 'Соц. дистанция'

    def __init__(self, group, pos_hero, ):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_hero[0] - self.radius, pos_hero[1] - self.radius
        self.group = group
        # self.pos = pos_hero
        self.live = FPS * 3.5
        self.live_timer = 0
        self.timer_damage = FPS // 3
        self.mobs_damaged = {}

        CORONA_VIRUS.play()

    def update(self, enemies):
        self.live_timer += 1
        if self.live_timer > self.live:
            self.kill()
        for enemy in enemies.copy():
            x, y = self.rect.x + self.radius - enemy.rect.centerx, self.rect.y + self.radius - enemy.rect.centery
            distance = math.sqrt(x * x + y * y)
            if distance <= self.radius:
                if enemy in self.mobs_damaged.keys():
                    self.mobs_damaged[enemy] += 1
                    if self.mobs_damaged[enemy] >= self.timer_damage:
                        enemy.hp -= self.damage
                        self.mobs_damaged[enemy] = 0
                else:
                    self.mobs_damaged[enemy] = 0
                    enemy.hp -= self.damage
            if enemy.hp <= 0:
                WELM_SCREAM.play()
                enemy.kill()


class Breastplate(pygame.sprite.Sprite):
    def __init__(self, hero):
        super().__init__()
        self.armor = 500
        self.image = pygame.image.load("Sprites/Creatures/нагрудник.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (22, 22))  # Пример размера
        self.rect = self.image.get_rect()
        self.hero = hero
        self.rect.center = (self.hero.rect.centerx - 3, self.hero.rect.centery + 2)  # Example offset

    def update(self, hero):
        self.rect.center = (hero.rect.centerx - 3, hero.rect.centery + 2)  # Example offset

    def upgrade_armor(self, hero):
        hero.armor += self.armor


class Boots(pygame.sprite.Sprite):
    def __init__(self, hero):
        super().__init__()
        self.armor = 250
        self.image = pygame.image.load("Sprites/Creatures/ботинки.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.rect = self.image.get_rect()
        self.hero = hero
        self.rect.center = (self.hero.rect.centerx - 3, self.hero.rect.centery + 15)

    def update(self, hero):
        self.rect.center = (hero.rect.centerx - 3, hero.rect.centery + 15)

    def upgrade_armor(self, hero):
        hero.armor += self.armor


weapons = {0: Needles, 1: Fireball, 2: SocialDistance}
items = {0: Breastplate, 1: Boots}


def get_weapon(index):
    return weapons[index]


def get_equipment(index):
    return items[index]


def find_index_weapon(weapon):
    for k, v in weapons.items():
        if v == weapon:
            return k

import pygame
import math
from Constants import FIELD_WIDTH, FIELD_HEIGHT

needle_image = pygame.image.load("Sprites/Creatures/needle_image.png").convert_alpha()
needle_image = pygame.transform.scale(needle_image, (30, 30))


# пока еще надо подумать, что и как

class Weapon(pygame.sprite.Sprite):  # там столько всего, что я думаю общим классом это не реализовать
    def __init__(self, group):
        super().__init__(group)
        self.image = None  # нужная картинка
        self.rect = self.image.get_rect()

    def update(self, event=None, tick=None):
        pass

    def draw(self, screen):
        pass


class Needles(pygame.sprite.Sprite):
    def __init__(self, group, pos_hero, enemies):
        super().__init__(group)
        self.image = needle_image  # Загруженное изображение иглы
        self.rect = self.image.get_rect(center=pos_hero)
        self.speed = 10
        self.damage = 50
        self.direction = self.get_direction(enemies)
        self.hit_targets = set()  # Запоминаем, кого уже поразили

    def spawn_needle(self):
        if not self.game_over:
            needle = Needles(self.needles, self.hero.rect.center, self.mobs)
            self.all_sprites.add(needle)

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
                    enemy.kill()  # Удаляем моба после смерти

        # Удаляем иглу, если она выходит за границы экрана
        if (self.rect.right < 0 or self.rect.left > FIELD_WIDTH or
                self.rect.bottom < 0 or self.rect.top > FIELD_HEIGHT):
            self.kill()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, group, pos_hero, enemies):
        super().__init__(group)
        self.image = pygame.image.load("фаербол.png")  # Загруженное изображение фаербола
        self.rect = self.image.get_rect(center=pos_hero)
        self.speed = 10
        self.damage = 50
        self.direction = self.get_direction(enemies)

    def spawn_fireball(self, group, pos_hero, enemies):
        fireball = Fireball(group, pos_hero, enemies)
        group.add(fireball)

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
                    enemy.kill()  # Удаляем моба после смерти
                self.kill()  # Фаербол исчезает после попадания
                break

        # Удаляем фаербол, если он выходит за границы экрана
        if (self.rect.right < 0 or self.rect.left > FIELD_WIDTH or
                self.rect.bottom < 0 or self.rect.top > FIELD_HEIGHT):
            self.kill()

class SocialDistance(pygame.sprite.Sprite):
    def __init__(self, group, pos_hero, radius=50, damage=30):
        super().__init__(group)
        self.group = group
        self.pos = pos_hero
        self.radius = radius
        self.damage = damage

    def spawn_social_distance(self, group, pos_hero):
        zone = SocialDistance(group, pos_hero)
        group.add(zone)

    def update(self, enemies):
        for enemy in enemies.copy():
            distance = math.hypot(self.pos[0] - enemy.rect.centerx, self.pos[1] - enemy.rect.centery)
            if distance <= self.radius:
                enemy.hp -= self.damage / 60  # Урон в секунду, делим на FPS
                if enemy.hp <= 0:
                    enemy.kill()



def get_weapon():
    pass

class Breastplate(pygame.sprite.Sprite):
    def __init__(self, hero):
        super().__init__()
        self.image = pygame.image.load("Sprites/Creatures/нагрудник.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (22, 22))  # Пример размера
        self.rect = self.image.get_rect()
        self.hero = hero
        self.rect.center = (self.hero.rect.centerx - 3, self.hero.rect.centery + 2)  # Example offset

    def update(self, hero):
        self.rect.center = (hero.rect.centerx - 3, hero.rect.centery + 2)  # Example offset

    def upgrade_armor(self, hero):
        hero.armor += 500

class Boots(pygame.sprite.Sprite):
    def __init__(self, hero):
        super().__init__()
        self.image = pygame.image.load("Sprites/Creatures/ботинки.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.rect = self.image.get_rect()
        self.hero = hero
        self.rect.center = (self.hero.rect.centerx - 3, self.hero.rect.centery + 15)

    def update(self, hero):
        self.rect.center = (hero.rect.centerx - 3, hero.rect.centery + 15)

    def upgrade_armor(self, hero):
        hero.armor += 250

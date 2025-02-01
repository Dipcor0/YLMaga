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

def get_weapon():
    pass

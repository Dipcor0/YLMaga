import pygame
import Constants


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


class Needles:
    def __init__(self, group):
        super().__init__(group)
        self.image = None  # нужная картинка
        self.rect = self.image.get_rect()

    def update(self, group_enemy, event=None, tick=None):
        pass

    def damage(self, enemy):
        pass

    def draw(self, screen, pos_hero):
        pass


def get_weapon():
    pass

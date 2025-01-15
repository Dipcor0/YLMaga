import pygame
import Constants


class Creature(pygame.sprite.Sprite):
    def __init__(self, group, image, pos):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, event=None):
        pass

    def draw(self, screen):
        pass


class Boss(Creature):
    def __init__(self, group, image, pos):
        super().__init__(group, image, pos)


class Enemy(Creature):
    def __init__(self, group, image, pos):
        super().__init__(group, image, pos)


class Hero(Creature):
    def __init__(self):
        super().__init__(Constants.GROUP_PLAYER, Constants.PLAYER_IMAGE, (0, 0))

    def update(self, event=None):
        pass

import pygame
from Constants import COLOR_SCREEN


class Shop:
    def __init__(self, hero):
        self.hero = hero

    def update(self, event=None):
        pass

    def draw(self, screen):
        screen.fill(COLOR_SCREEN)

    def _change_scene(self, scene: int):
        pass


class Battle:
    def __init__(self, hero):
        self.hero = hero

    def update(self, event=None):
        pass

    def draw(self, screen):
        screen.fill('blue')

    def _change_scene(self, scene: int):
        pass

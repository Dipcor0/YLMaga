import pygame


class Creature:
    def __init__(self):
        pass

    def update(self, event=None):
        pass

    def draw(self, screen):
        pass


class Boss(Creature):
    def __init__(self):
        super().__init__()


class Enemy(Creature):
    def __init__(self):
        super().__init__()


class Hero(Creature):
    def __init__(self):
        super().__init__()

    def update(self, event=None):
        pass

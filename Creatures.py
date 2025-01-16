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
        self.speed = Constants.PLAYER_SPEED_MOVE
        self.coord_x = 500                                            # куча данных персонажа. От сюда
        self.coord_y = 500
        self.level = Constants.PLAYER_LEVEL
        self.hp = Constants.PLAYER_HP
        self.regen = Constants.PLAYER_REGEN
        self.hit = Constants.PLAYER_HIT
        self.chane_crit = Constants.PLAYER_CHANCE_CRIT
        self.koef_krit = Constants.PLAYER_KOEF_CRIT
        self.armor = Constants.PLAYER_ARMOR
        self.chance_avoidence = Constants.PLAYER_CHANCE_AVOIDANCE    # До сюда
        self.inventory = []
    def update(self, event=None):
        if event.key == pygame.K_w:
            self.move(0, -self.speed)
        if event.key == pygame.K_s:
            self.move(0, self.speed)
        if event.key == pygame.K_a:
            self.move(-self.speed, 0)
        if event.key == pygame.K_d:
            self.move(self.speed, 0)

    def move(self, dx, dy): # изменение координаты во время движения
      self.coord_x += dx
      self.coord_y += dy

    def get_coords(self):
        return [self.coord_x, self.coord_y]

    def get_hp(self):
        return self.hp

    def get_armor(self):
        return self.armor

    def get_inventory(self):
        return self.inventory

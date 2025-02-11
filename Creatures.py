import pygame
import Constants
import Equipment
from Constants import PLAYER_SPEED_MOVE, FIELD_HEIGHT, FIELD_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/Creatures/персонаж.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (Constants.SIZE_SCREEN[0] // 2 - self.image.get_width() // 2,
                            Constants.SIZE_SCREEN[1] // 2 - self.image.get_height() // 2)
        self.speed = PLAYER_SPEED_MOVE
        self.weapons = {}
        self.load_weapon()
        self.inventory = []
        self.load_inventory()
        self.can_move = True

    def update(self, scene=None):
        if self.can_move:
            if not scene:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and self.rect.top > 0:
                    self.rect.y -= self.speed
                if keys[pygame.K_s] and self.rect.bottom < FIELD_HEIGHT:
                    self.rect.y += self.speed
                if keys[pygame.K_a] and self.rect.left > 0:
                    self.rect.x -= self.speed
                if keys[pygame.K_d] and self.rect.right < FIELD_WIDTH:
                    self.rect.x += self.speed
            elif scene == 1:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and self.rect.top > 0:
                    self.rect.y -= self.speed
                if keys[pygame.K_s] and self.rect.bottom < Constants.SIZE_SCREEN[1]:
                    self.rect.y += self.speed
                if keys[pygame.K_a] and self.rect.left > 0:
                    self.rect.x -= self.speed
                if keys[pygame.K_d] and self.rect.right < Constants.SIZE_SCREEN[0]:
                    self.rect.x += self.speed

        for item in self.inventory:
            item.update(self)

    def load_inventory(self):
        self.inventory.clear()
        for index in Constants.PLAYER_EQUIPMENT:
            self.inventory.append(Equipment.get_equipment(index)(self))

    def load_weapon(self):
        self.weapons.clear()
        for index in Constants.PLAYER_WEAPON:
            weapon = Equipment.get_weapon(index)
            self.weapons[(weapon, index)] = [weapon.reload, 0]  # оружие: кд, таймер

    def block_move(self):
        self.can_move = not self.can_move


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


class Boar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Constants.BOAR_IMAGE  # Добавь изображение кабана в Constants
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1  # Медленнее обычного моба
        self.attack_cooldown = 1500  # Дольше между атаками
        self.last_attack_time = pygame.time.get_ticks()
        self.hp = 200  # Увеличенное здоровье
        self.damage = 20  # Более сильная атака

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

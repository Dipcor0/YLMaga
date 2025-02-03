import pygame
import Constants
import Equipment
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, PLAYER_HP, PLAYER_ARMOR, RED, WHITE, SLOT_SIZE, INVENTORY_SLOTS, \
    FIELD_HEIGHT, FIELD_WIDTH, FPS, GRAY

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
        self.weapon = None
        self.load_weapon()
        self.inventory = []
        self.load_inventory()

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

        for item in self.inventory:
            item.update(self)

    def load_inventory(self):
        for index in Constants.PLAYER_EQUIPMENT:
            self.inventory.append(Equipment.get_equipment(index)(self))

    def load_weapon(self):
        self.weapon = Equipment.get_weapon(Constants.PLAYER_WEAPON)


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

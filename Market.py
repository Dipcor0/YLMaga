import pygame

import Constants
import Constants
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, PLAYER_HP, PLAYER_ARMOR, RED, WHITE, SLOT_SIZE, INVENTORY_SLOTS, \
    FIELD_HEIGHT, FIELD_WIDTH, FPS, GRAY, SIZE_ZONE_STORE, SIZE_SCREEN


class Shop:
    def __init__(self, hero):
        self.hero = hero
        self.armor = PLAYER_ARMOR
        self.hp = PLAYER_HP
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.hero)
        self.fight = Fight((SIZE_SCREEN[0] // 2 - SIZE_ZONE_STORE[0] // 2, 0), self.hero, self.all_sprites)
        self.store = Store((0, SIZE_SCREEN[1] // 4), self.hero, self.all_sprites)
        self.upgrade = Upgrade((SIZE_SCREEN[0] - SIZE_ZONE_STORE[0], SIZE_SCREEN[1] // 4), self.hero, self.all_sprites)

        self.flag_fight = False
        for item in self.hero.inventory:
            self.all_sprites.add(item)
            item.upgrade_armor(self)

    def update_all(self, event=None, tick=None):
        self.hero.update(1)
        self.store.update(event)
        self.upgrade.update(event)
        self.fight.update(event)
        if self.fight.flag_set_fight:
            self.flag_fight = True
            self.fight.flag_set_fight = False

    def draw_all(self, screen):
        screen.blit(Constants.BACKGROUND_MARKET_IMAGE, (0, 0))
        self.all_sprites.draw(screen)
        self.store.draw(screen)
        self.upgrade.draw(screen)
        self.fight.draw(screen)

    def _change_scene(self, scene: int):
        pass


class Store:
    player_in_zone = False
    open_window = False

    def __init__(self, pos, hero, group_player):
        self.pos = pos
        self.group = group_player
        self.zone = pygame.sprite.Sprite()
        self.zone.image = pygame.Surface(SIZE_ZONE_STORE)
        self.zone.image.fill((0, 0, 0))
        self.zone.rect = self.zone.image.get_rect()
        self.zone.rect.x, self.zone.rect.y = pos
        self.font = pygame.font.Font(None, 36)
        self.mes = self.font.render('E', True, WHITE)
        self.hero = hero

    def update(self, event=None):
        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not self.open_window and self.player_in_zone:
                    self.open_window = True
                    # self.hero.block_move()
                elif event.key == pygame.K_e and self.open_window:
                    self.open_window = False
                    # self.hero.block_move()
        else:
            if pygame.sprite.spritecollideany(self.zone, self.group):
                self.player_in_zone = True

            else:
                self.player_in_zone = False
        # TODO: дальше делать магазин :)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('red'), (*self.pos, *SIZE_ZONE_STORE), width=1)

        if self.player_in_zone:
            screen.blit(self.mes, (self.pos[0] + SIZE_ZONE_STORE[0] // 2, self.pos[1] + SIZE_ZONE_STORE[1] // 2))
        if self.open_window:
            pygame.draw.rect(screen, pygame.Color('blue'), (50, 50, SIZE_SCREEN[0] - 100, SIZE_SCREEN[1] - 100),
                             width=0)


class Upgrade:
    player_in_zone = False
    open_window = False

    def __init__(self, pos, hero, group_player):
        self.pos = pos
        self.group = group_player
        self.zone = pygame.sprite.Sprite()
        self.zone.image = pygame.Surface(SIZE_ZONE_STORE)
        self.zone.image.fill((0, 0, 0))
        self.zone.rect = self.zone.image.get_rect()
        self.zone.rect.x, self.zone.rect.y = pos
        self.font = pygame.font.Font(None, 36)
        self.mes = self.font.render('E', True, WHITE)
        self.hero = hero

    def update(self, event=None):
        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not self.open_window and self.player_in_zone:
                    self.open_window = True
                    # self.hero.block_move()
                elif event.key == pygame.K_e and self.open_window:
                    self.open_window = False
                    # self.hero.block_move()
        else:
            if pygame.sprite.spritecollideany(self.zone, self.group):
                self.player_in_zone = True

            else:
                self.player_in_zone = False
        # TODO: дальше делать магазин :)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('red'), (*self.pos, *SIZE_ZONE_STORE), width=1)

        if self.player_in_zone:
            screen.blit(self.mes, (self.pos[0] + SIZE_ZONE_STORE[0] // 2, self.pos[1] + SIZE_ZONE_STORE[1] // 2))
        if self.open_window:
            pygame.draw.rect(screen, pygame.Color('blue'), (50, 50, SIZE_SCREEN[0] - 100, SIZE_SCREEN[1] - 100),
                             width=0)


class Fight:
    player_in_zone = False

    def __init__(self, pos, hero, group_player):
        self.pos = pos
        self.group = group_player
        self.zone = pygame.sprite.Sprite()
        self.zone.image = pygame.Surface(SIZE_ZONE_STORE)
        self.zone.image.fill((0, 0, 0))
        self.zone.rect = self.zone.image.get_rect()
        self.zone.rect.x, self.zone.rect.y = pos
        self.font = pygame.font.Font(None, 36)
        self.mes = self.font.render('E', True, WHITE)
        self.hero = hero

        self.flag_set_fight = False

    def update(self, event=None):
        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and self.player_in_zone:
                    self.flag_set_fight = True
        else:
            if pygame.sprite.spritecollideany(self.zone, self.group):
                self.player_in_zone = True

            else:
                self.player_in_zone = False
        # TODO: дальше делать магазин :)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('red'), (*self.pos, *SIZE_ZONE_STORE), width=1)

        if self.player_in_zone:
            screen.blit(self.mes, (self.pos[0] + SIZE_ZONE_STORE[0] // 2, self.pos[1] + SIZE_ZONE_STORE[1] // 2))

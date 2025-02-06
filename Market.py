import pygame
from MarketTools import WindowStore
import Constants
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, PLAYER_HP, PLAYER_ARMOR, RED, WHITE, SLOT_SIZE, INVENTORY_SLOTS, \
    FIELD_HEIGHT, FIELD_WIDTH, FPS, GRAY, SIZE_ZONE_STORE, SIZE_SCREEN, BLUE, SIZE_BOX, DARK_BLUE, DARK_DARK_BLUE, \
    LIGHT_BLUE, BLACK


def update_inventory(all_sp, hero):
    all_sp.empty()
    all_sp.add(hero)
    hero.load_inventory()
    for item in hero.inventory:
        all_sp.add(item)


class Shop:
    def __init__(self, hero):
        self.font = pygame.font.Font(None, 36)

        self.hero = hero
        self.armor = PLAYER_ARMOR
        self.hp = PLAYER_HP

        self.all_sprites = pygame.sprite.Group()
        self.fight = Fight((SIZE_SCREEN[0] // 2 - Constants.TELEPORT_FIGHT.get_width() // 2, 0), self.hero,
                           self.all_sprites)
        self.store = Store((0, SIZE_SCREEN[1] // 4), self.hero, self.all_sprites)
        self.upgrade = Upgrade((SIZE_SCREEN[0] - SIZE_ZONE_STORE[0], SIZE_SCREEN[1] // 4), self.hero, self.all_sprites)

        self.flag_fight = False
        update_inventory(self.all_sprites, self.hero)

    def update_all(self, event=None, tick=None):
        if len(self.all_sprites) - 1 != len(Constants.PLAYER_EQUIPMENT):
            update_inventory(self.all_sprites, self.hero)
        if event is None:
            self.hero.update(1)
        self.store.update(event)
        self.upgrade.update(event)
        self.fight.update(event)
        if self.fight.flag_set_fight:
            self.flag_fight = True
            self.fight.flag_set_fight = False

    def draw_all(self, screen):
        screen.blit(Constants.BACKGROUND_MARKET_IMAGE, (0, 0))
        self.fight.draw(screen)

        self.all_sprites.draw(screen)

        self.store.draw(screen)
        self.upgrade.draw(screen)

        self.upgrade.draw_window(screen)
        self.store.draw_window(screen)

        text = self.font.render(f'GOLD: {Constants.MONEY} CRYSTALS: {Constants.CRYSTALS}', True, DARK_BLUE)
        pygame.draw.rect(screen, BLUE, (0, 0, text.get_width(), text.get_height()))
        screen.blit(text, (0, 0))

    def reboot(self):
        update_inventory(self.all_sprites, self.hero)


class Store:
    player_in_zone = False
    open_window = False

    def __init__(self, pos, hero, group_player):
        self.pos = pos
        self.group = group_player

        self.zone = pygame.sprite.Sprite()
        self.zone.image = Constants.SHOP_IMAGE
        # self.zone.image.fill((0, 0, 0))
        self.zone.rect = self.zone.image.get_rect()
        self.zone.rect.x, self.zone.rect.y = pos

        self.font = pygame.font.Font(None, 36)
        self.mes = self.font.render('E', True, WHITE)

        self.hero = hero
        self.window = WindowStore()

    def update(self, event=None):
        if event:
            self.window.update(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not self.open_window and self.player_in_zone:
                    self.open_window = True
                    self.window.open()
                    self.hero.block_move()
                elif event.key == pygame.K_e and self.open_window:
                    self.open_window = False
                    self.window.close()
                    self.hero.block_move()
        else:
            if pygame.sprite.spritecollideany(self.zone, self.group):
                self.player_in_zone = True
            else:
                self.player_in_zone = False

    def draw(self, screen):
        screen.blit(self.zone.image, (self.pos[0] + SIZE_ZONE_STORE[0] // 2 - self.zone.image.get_width() // 2,
                                      self.pos[1] + SIZE_ZONE_STORE[1] // 2 - self.zone.image.get_height() // 2))

        if self.player_in_zone:
            screen.blit(self.mes, (self.pos[0] + SIZE_ZONE_STORE[0] // 2, self.pos[1] + SIZE_ZONE_STORE[1] // 2))

    def draw_window(self, screen):
        if self.open_window:
            self.window.draw(screen)


class Upgrade:
    player_in_zone = False
    open_window = False

    def __init__(self, pos, hero, group_player):
        self.pos = pos

        self.group = group_player

        self.ball = Constants.UPGRADE_MAGIC_BALL_IMAGE
        self.hands = Constants.UPGRADE_MAGIC_HANDS_IMAGE
        self.hands_pos = 0
        self.zone = pygame.sprite.Sprite()
        self.zone.image = self.ball
        self.zone.rect = self.zone.image.get_rect()
        self.zone.rect.x, self.zone.rect.y = pos

        self.font = pygame.font.Font(None, 36)
        self.mes = self.font.render('E', True, (135, 0, 219))

        self.hero = hero

    def update(self, event=None):
        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not self.open_window and self.player_in_zone:
                    self.open_window = True
                    self.hero.block_move()
                elif event.key == pygame.K_e and self.open_window:
                    self.open_window = False
                    self.hero.block_move()

        else:
            if pygame.sprite.spritecollideany(self.zone, self.group):
                self.player_in_zone = True

            else:
                self.player_in_zone = False
        # TODO: дальше делать магазин :)

    def draw(self, screen):
        screen.blit(self.zone.image, self.pos)
        screen.blit(self.hands, self.pos)

        if self.player_in_zone:
            screen.blit(self.mes, (self.pos[0] + self.zone.image.get_width() // 2 - 5,
                                   self.pos[1] + self.zone.image.get_height() // 2 + 20))

    def draw_window(self, screen):
        if self.open_window:
            pygame.draw.rect(screen, BLUE, (50, 50, SIZE_SCREEN[0] - 100, SIZE_SCREEN[1] - 100),
                             width=0)
            screen.blit(self.font.render('В разроботке', True, (135, 0, 219)), (50, 50))


class Fight:
    player_in_zone = False

    def __init__(self, pos, hero, group_player):
        self.pos = pos
        self.group = group_player
        self.activ = Constants.TELEPORT_FIGHT_ACTIVE
        self.dis_activ = Constants.TELEPORT_FIGHT
        self.zone = pygame.sprite.Sprite()
        self.zone.image = self.dis_activ
        self.zone.rect = self.zone.image.get_rect()
        self.zone.rect.x, self.zone.rect.y = self.pos
        self.font = pygame.font.Font(None, 36)
        self.mes = self.font.render('E', True, BLUE)
        self.flag_set_fight = False

    def update(self, event=None):
        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and self.player_in_zone:
                    self.flag_set_fight = True
        else:
            if pygame.sprite.spritecollideany(self.zone, self.group):
                self.player_in_zone = True
                self.zone.image = self.activ

            else:
                self.player_in_zone = False
                self.zone.image = self.dis_activ

    def draw(self, screen):
        screen.blit(self.zone.image, self.zone.rect)

        if self.player_in_zone:
            screen.blit(self.mes, (
                self.pos[0] + self.zone.image.get_width() // 2 - 8,
                self.pos[1] + self.zone.image.get_height() // 2 - 8))

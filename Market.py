import pygame

import Constants
import Equipment
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, PLAYER_HP, PLAYER_ARMOR, RED, WHITE, SLOT_SIZE, INVENTORY_SLOTS, \
    FIELD_HEIGHT, FIELD_WIDTH, FPS, GRAY, SIZE_ZONE_STORE, SIZE_SCREEN, BLUE, SIZE_BOX, DARK_BLUE, DARK_DARK_BLUE, \
    LIGHT_BLUE, BLACK


class Shop:
    def __init__(self, hero):
        self.font = pygame.font.Font(None, 36)

        self.hero = hero

        self.armor = PLAYER_ARMOR
        self.hp = PLAYER_HP

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.hero)
        self.fight = Fight((SIZE_SCREEN[0] // 2 - Constants.TELEPORT_FIGHT.get_width() // 2, 0), self.hero,
                           self.all_sprites)
        self.store = Store((0, SIZE_SCREEN[1] // 4), self.hero, self.all_sprites)
        self.upgrade = Upgrade((SIZE_SCREEN[0] - SIZE_ZONE_STORE[0], SIZE_SCREEN[1] // 4), self.hero, self.all_sprites)

        self.flag_fight = False
        for item in self.hero.inventory:
            self.all_sprites.add(item)
            item.upgrade_armor(self)

    def update_all(self, event=None, tick=None):
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
        # TODO: дальше делать магазин :)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('red'), (*self.pos, *SIZE_ZONE_STORE), width=1)

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


class WindowStore:
    def __init__(self):
        self.top = 50
        self.left = 100
        self.font = pygame.font.Font(None, 81)
        self.head1 = self.font.render('Оружие', True, DARK_BLUE)
        self.head1_pos = 20, 10
        self.opened = False
        self.items = []
        base = [(Equipment.Needles, 52), (Equipment.Fireball, 40), (Equipment.SocialDistance, 100)]
        for index in range(len(base)):
            self.items.append(ItemStoreWeapon(*base[index],
                                              (self.left + self.head1_pos[0] + (SIZE_BOX[0] + 20) * index,
                                               self.top + self.head1.get_height() + self.head1_pos[1] + 10)))

    def open(self):
        self.opened = True

    def close(self):
        self.opened = False

    def update(self, event):
        if self.opened:
            for it in self.items:
                it.update(event)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE,
                         (self.left, self.top, SIZE_SCREEN[0] - self.left * 2, SIZE_SCREEN[1] - self.top * 2),
                         width=0)
        screen.blit(self.head1, (self.head1_pos[0] + self.left, self.head1_pos[1] + self.top))
        [it.draw(screen) for it in self.items]


class ItemStoreWeapon:
    def __init__(self, item, cost, pos):
        self.pos = pos

        self.index_item = Equipment.find_index_weapon(item)
        self.image = pygame.transform.scale(item.image, (30, 30))
        self.name = item.name
        self.text = {'reload piec/s': None, 'speed pix/s': None, 'damage hp': None}
        self.cost = cost

        self.font = pygame.font.Font(None, 30)
        rect_btn = (self.pos[0] + SIZE_BOX[0] // 6,
                    self.pos[1] + SIZE_BOX[1] * 5 // 6 - 10,
                    SIZE_BOX[0] * 4 // 6,
                    SIZE_BOX[1] // 6)
        self.btn = Button(self, f'КУПИТЬ {self.cost}G', Constants.ALL_WEAPON,
                          Constants.PLAYER_WEAPON, self.index_item, rect_btn, cost)

        if self.index_item in Constants.ALL_WEAPON:
            self.btn.not_buying()

        for k, lm in {'reload piec/s': (lambda x: FPS / x.reload), 'speed pix/s': (lambda x: x.speed),
                      'damage hp': (lambda x: x.damage)}.items():
            try:
                res = lm(item)
                self.text[k] = res
            except Exception:
                pass

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_BLUE, (*self.pos, *SIZE_BOX), width=0)

        screen.blit(self.image, (self.pos[0] + SIZE_BOX[0] // 2 - self.image.get_width() // 2,
                                 self.pos[1] + SIZE_BOX[1] // 6 - self.image.get_height() // 2))
        name = self.font.render(self.name, True, BLUE)
        screen.blit(name, (self.pos[0] + SIZE_BOX[0] // 2 - name.get_width() // 2,
                           self.pos[1] + SIZE_BOX[1] // 6 + self.image.get_height()))
        i = 0
        for k, v in self.text.items():
            if v:
                res_pos = (
                    self.pos[0],
                    self.pos[1] + SIZE_BOX[1] // 6 + self.image.get_height() + name.get_height() + 25 * i)
                screen.blit(self.font.render(f'{k}: {v}', True, BLUE), res_pos)
                i += 1
        self.btn.draw(screen)

    def update(self, event):
        self.btn.update(event)


class Button:
    def __init__(self, board, text, all_group, player_group, index_item, rect, cost):
        self.board = board
        self.text = text
        self.index_item = index_item
        self.all_group = all_group
        self.player_group = player_group
        self.rect = rect
        self.cost = cost

        self.buying = True
        self.color = LIGHT_BLUE

        self.font = pygame.font.Font(None, 25)
        self.in_zone = False

    def update(self, event):
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            if self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2] and \
                    self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3]:
                self.in_zone = True
            else:
                self.in_zone = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.in_zone and self.buying and Constants.MONEY >= self.cost:
                Constants.MONEY -= self.cost
                self.not_buying()
                self.all_group.append(self.index_item)
                self.player_group.append(self.index_item)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=0)
        text = self.font.render(self.text, True, WHITE)
        pos = (self.rect[0] + self.rect[2] // 2 - text.get_width() // 2,
               self.rect[1] + self.rect[3] // 2 - text.get_height() // 2)
        screen.blit(text, pos)

        if self.buying and self.in_zone:
            pygame.draw.rect(screen, WHITE, self.rect, width=5)

    def not_buying(self):
        self.buying = False
        self.color = DARK_DARK_BLUE

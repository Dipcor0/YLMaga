import pygame
from Constants import SIZE_SCREEN, SIZE_ZONE_STORE, COLOR_SCREEN, GROUP_PLAYER, WHITE


class Shop:
    def __init__(self, hero):
        self.hero = hero
        self.store = Store((0, SIZE_SCREEN[1] // 4), self.hero)
        self.upgrade = Upgrade((SIZE_SCREEN[0] - SIZE_ZONE_STORE[0], SIZE_SCREEN[1] // 4), self.hero)

    def update(self, event=None, tick=None):
        self.store.update()
        self.upgrade.update()
        if event:
            if event.type == pygame.KEYDOWN:
                self.store.update(event)
                self.upgrade.update(event)

    def draw(self, screen):
        screen.fill(COLOR_SCREEN)
        GROUP_PLAYER.draw(screen)
        self.store.draw(screen)
        self.upgrade.draw(screen)

    def _change_scene(self, scene: int):
        pass


class Battle:
    def __init__(self, hero):
        self.hero = hero

    def update(self, event=None, tick=None):
        pass

    def draw(self, screen):
        screen.fill('blue')

    def _change_scene(self, scene: int):
        pass


class Store:
    player_in_zone = False
    open_window = False

    def __init__(self, pos, hero):
        self.pos = pos
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
                    self.hero.block_move()
                elif event.key == pygame.K_e and self.open_window:
                    self.open_window = False
                    self.hero.block_move()
        else:
            if pygame.sprite.spritecollideany(self.zone, GROUP_PLAYER):
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

    def __init__(self, pos, hero):
        self.pos = pos
        self.zone = pygame.sprite.Sprite()
        self.zone.image = pygame.Surface(SIZE_ZONE_STORE)
        self.zone.image.fill((0, 0, 0))
        self.zone.rect = self.zone.image.get_rect()
        self.zone.rect.x, self.zone.rect.y = pos
        self.font = pygame.font.Font(None, 36)
        self.mes = self.font.render('E', True, WHITE)
        self.hero = hero

    def update(self, event=None):
        self.hero.update()
        if event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not self.open_window and self.player_in_zone:
                    self.open_window = True
                    self.hero.block_move()
                elif event.key == pygame.K_e and self.open_window:
                    self.open_window = False
                    self.hero.block_move()
        else:
            if pygame.sprite.spritecollideany(self.zone, GROUP_PLAYER):
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

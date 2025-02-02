import pygame
import random
from Equipment import Needles, Breastplate, Boots, Fireball
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, PLAYER_HP, PLAYER_ARMOR, RED, WHITE, SLOT_SIZE, INVENTORY_SLOTS, \
    FIELD_HEIGHT, FIELD_WIDTH, FPS, GRAY
import Constants
import Creatures


# Интерфейс
class Interface:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.hp = PLAYER_HP
        self.armor = PLAYER_ARMOR
        self.exp = 0
        self.coins = 0
        self.crystals = 0

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, (0, FIELD_HEIGHT, FIELD_WIDTH, UI_HEIGHT))
        surface.blit(Constants.HEART_IMAGE, (10, FIELD_HEIGHT + 10))
        surface.blit(Constants.ARMOR_IMAGE, (10, FIELD_HEIGHT + 50))
        surface.blit(Constants.CRYSTAL_IMAGE, (10, FIELD_HEIGHT + 90))
        surface.blit(Constants.COIN_IMAGE, (10, FIELD_HEIGHT + 130))

        hp_text = self.font.render(f"{self.hp}", True, WHITE)
        armor_text = self.font.render(f"{self.armor}", True, WHITE)
        crystal_text = self.font.render(f"{self.crystals}", True, WHITE)
        coin_text = self.font.render(f"{self.coins}", True, WHITE)

        surface.blit(hp_text, (50, FIELD_HEIGHT + 10))
        surface.blit(armor_text, (50, FIELD_HEIGHT + 50))
        surface.blit(crystal_text, (50, FIELD_HEIGHT + 90))
        surface.blit(coin_text, (50, FIELD_HEIGHT + 130))

        slot_size = SLOT_SIZE
        for i in range(INVENTORY_SLOTS):
            slot_x = 200 + i * (slot_size + 10)
            slot_y = FIELD_HEIGHT + 10
            pygame.draw.rect(surface, GRAY, (slot_x, slot_y, slot_size, slot_size), 2)


# Битва
class Battle:
    def __init__(self, hero):
        self.hero = hero
        self.mobs = pygame.sprite.Group()
        self.needles = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.hero)
        self.ui = Interface()
        self.spawn_timer = 0
        self.game_over = False

        self.breastplate = Breastplate(self.hero)
        self.all_sprites.add(self.breastplate)
        self.breastplate.upgrade_armor(self.ui)

        self.boots = Boots(self.hero)
        self.all_sprites.add(self.boots)
        self.boots.upgrade_armor(self.ui)

    def spawn_mob(self):
        if not self.game_over:
            x = random.randint(0, FIELD_WIDTH)
            y = random.randint(0, FIELD_HEIGHT)
            mob = Creatures.Mob(x, y)
            self.mobs.add(mob)
            self.all_sprites.add(mob)

    def spawn_fireball(self):
        if not self.game_over:
            fireball = Fireball(self.fireballs, self.hero.rect.center, self.mobs)
            self.all_sprites.add(fireball)

    def check_collisions(self):
        for mob in self.mobs.copy():
            if self.hero.rect.colliderect(mob.rect) and mob.can_attack():
                if self.ui.armor > 0:
                    self.ui.armor -= 10
                else:
                    self.ui.hp -= 10
                if self.ui.hp <= 0:
                    self.game_over = True

            if mob.hp <= 0:
                mob.kill()  # Удаляем моба, если его здоровье <= 0

    def update_all(self):
        if not self.game_over:
            self.hero.update()
            self.breastplate.update(self.hero)
            self.boots.update(self.hero)
            self.mobs.update(self.hero)
            self.needles.update(self.mobs)
            self.fireballs.update(self.mobs)
            self.check_collisions()

            self.spawn_timer += 1
            if self.spawn_timer > FPS * 2:
                self.spawn_mob()
                self.spawn_fireball()
                self.spawn_timer = 0

    def draw_all(self, screen):
        screen.blit(Constants.BACKGROUND_IMAGE, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, 0, FIELD_WIDTH, FIELD_HEIGHT), 5)
        self.all_sprites.draw(screen)
        self.ui.draw(screen)

        if self.game_over:
            game_over_text = self.ui.font.render("GAME OVER. PRESS ESC", True, RED)
            screen.blit(game_over_text, (FIELD_WIDTH // 2 - 100, FIELD_HEIGHT // 2 - 50))

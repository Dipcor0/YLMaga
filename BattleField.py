import pygame
import random
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
        self.group_weapon = pygame.sprite.Group()
        self.weapon = self.hero.weapon
        self.all_sprites = pygame.sprite.Group(self.hero)
        self.ui = Interface()
        self.spawn_timer = 0
        self.reload = self.weapon.reload
        self.reload_timer = 0
        self.game_over = False

        for item in self.hero.inventory:
            self.all_sprites.add(item)
            item.upgrade_armor(self.ui)

    def spawn_weapon(self):
        if Constants.PLAYER_WEAPON != 2:
            weapon = self.weapon(self.group_weapon, self.hero.rect.center, self.mobs)
        else:
            weapon = self.weapon(self.group_weapon, self.hero.rect.center)
        self.all_sprites.add(weapon)

    def spawn_mob(self):
        if not self.game_over:
            x = random.randint(0, FIELD_WIDTH)
            y = random.randint(0, FIELD_HEIGHT)
            mob = Creatures.Mob(x, y)
            self.mobs.add(mob)
            self.all_sprites.add(mob)

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
            self.mobs.update(self.hero)
            self.group_weapon.update(self.mobs)
            self.check_collisions()

            self.spawn_timer += 1
            self.reload_timer += 1
            if self.spawn_timer > FPS * 2:
                self.spawn_mob()
                self.spawn_timer = 0
            if self.reload_timer > self.reload:
                self.spawn_weapon()
                self.reload_timer = 0

    def draw_all(self, screen):
        screen.blit(Constants.BACKGROUND_IMAGE, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, 0, FIELD_WIDTH, FIELD_HEIGHT), 5)
        self.all_sprites.draw(screen)
        self.ui.draw(screen)

        if self.game_over:
            game_over_text = self.ui.font.render("GAME OVER. PRESS ESC", True, RED)
            screen.blit(game_over_text, (FIELD_WIDTH // 2 - 100, FIELD_HEIGHT // 2 - 50))

import pygame
import random
from Equipment import Needles
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, PLAYER_HP, PLAYER_ARMOR, RED, WHITE, SLOT_SIZE, INVENTORY_SLOTS, FIELD_HEIGHT, FIELD_WIDTH, FPS, GRAY

# Инициализация Pygame
pygame.init()

# Окно игры
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("BattleGame")
clock = pygame.time.Clock()
 

# Загрузка изображений
background_image = pygame.image.load("Sprites/Creatures/полеБоя.png").convert_alpha()
background_image = pygame.transform.scale(background_image, (FIELD_WIDTH, FIELD_HEIGHT))

heart_image = pygame.image.load("Sprites/Creatures/сердце.png").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (30, 30))

armor_image = pygame.image.load("Sprites/Creatures/броня.png").convert_alpha()
armor_image = pygame.transform.scale(armor_image, (30, 30))

crystal_image = pygame.image.load("Sprites/Creatures/кристалик.png").convert_alpha()
crystal_image = pygame.transform.scale(crystal_image, (30, 30))

coin_image = pygame.image.load("Sprites/Creatures/монетка.png").convert_alpha()
coin_image = pygame.transform.scale(coin_image, (30, 30))

mob_image = pygame.image.load("Sprites/Creatures/моб.png").convert_alpha()
mob_image = pygame.transform.scale(mob_image, (60, 60))  # Увеличен размер мобов



# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/Creatures/персонаж.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2)
        self.speed = PLAYER_SPEED_MOVE

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


# Моб
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = mob_image
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
        surface.blit(heart_image, (10, FIELD_HEIGHT + 10))
        surface.blit(armor_image, (10, FIELD_HEIGHT + 50))
        surface.blit(crystal_image, (10, FIELD_HEIGHT + 90))
        surface.blit(coin_image, (10, FIELD_HEIGHT + 130))

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
    def __init__(self):
        self.hero = Player()
        self.mobs = pygame.sprite.Group()
        self.needles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.hero)
        self.ui = Interface()
        self.spawn_timer = 0
        self.game_over = False

    def spawn_needle(self):
        if not self.game_over:
            needle = Needles(self.needles, self.hero.rect.center, self.mobs)
            self.all_sprites.add(needle)

    def spawn_mob(self):
        if not self.game_over:
            x = random.randint(0, FIELD_WIDTH)
            y = random.randint(0, FIELD_HEIGHT)
            mob = Mob(x, y)
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
            self.needles.update(self.mobs)
            self.check_collisions()

            self.spawn_timer += 1
            if self.spawn_timer > FPS * 2:
                self.spawn_mob()
                self.spawn_needle()
                self.spawn_timer = 0

    def draw_all(self, screen):
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, WHITE, (0, 0, FIELD_WIDTH, FIELD_HEIGHT), 5)
        self.all_sprites.draw(screen)
        self.ui.draw(screen)

        if self.game_over:
            game_over_text = self.ui.font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (FIELD_WIDTH // 2 - 100, FIELD_HEIGHT // 2 - 50))


# Основной цикл
battle = Battle()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    battle.update_all()
    battle.draw_all(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

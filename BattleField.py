import pygame
import random
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, RED, PLAYER_HP, PLAYER_ARMOR, BLUE, WHITE, SLOT_SIZE, INVENTORY_SLOTS, FPS, GRAY, BLACK

# Инициализация Pygame
pygame.init()

# Инициализация окна
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("BattleGame")
clock = pygame.time.Clock()

# Получение размеров экрана
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
FIELD_WIDTH = SCREEN_WIDTH
FIELD_HEIGHT = SCREEN_HEIGHT - UI_HEIGHT

# Игрок, который прописан в битве короче ГОЙДА хихихиха мне есть грусть он изначально был зеленым квадратом(((
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/Creatures/персонаж.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 50))  # Изменение размера спрайта персонажа
        self.rect = self.image.get_rect()
        self.rect.center = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2) # я так понял спавн на середине
        self.speed = PLAYER_SPEED_MOVE # я

    def update(self): # Кнопки на васд
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
class Mob(pygame.sprite.Sprite): # мобы пока красные квадратики...
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self, target): # ходьба мобов
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        if self.rect.x > target.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        if self.rect.y > target.rect.y:
            self.rect.y -= self.speed

# Инвентарь и информация
class Interface:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.hp = PLAYER_HP
        self.armor = PLAYER_ARMOR
        self.exp = 0

    def draw(self, surface):
        # Рисуем область для для интерфейса
        pygame.draw.rect(surface, BLUE, (0, FIELD_HEIGHT, SCREEN_WIDTH, UI_HEIGHT)) #  пусть пока сининький
        hp_text = self.font.render(f"HP: {self.hp}", True, WHITE)  # а текст беленький
        armor_text = self.font.render(f"Armor: {self.armor}", True, WHITE)
        exp_text = self.font.render(f"EXP: {self.exp}", True, WHITE)
        exit_text = self.font.render("Esc - выйти из игры", True, WHITE)

        surface.blit(hp_text, (10, FIELD_HEIGHT + 10))
        surface.blit(armor_text, (10, FIELD_HEIGHT + 50))
        surface.blit(exp_text, (10, FIELD_HEIGHT + 90))
        surface.blit(exit_text, (10, FIELD_HEIGHT + 140))

        # Рисуем ячейки инвентаря
        slot_size = SLOT_SIZE
        for i in range(INVENTORY_SLOTS):
            slot_x = 200 + i * (slot_size + 10)
            slot_y = FIELD_HEIGHT + 10
            pygame.draw.rect(surface, GRAY, (slot_x, slot_y, slot_size, slot_size), 2)

# Битва
class Battle:
    def __init__(self):
        self.player = Player()
        self.mobs = pygame.sprite.Group() # делаем группу спрайтов врагов
        self.all_sprites = pygame.sprite.Group(self.player)
        self.ui = Interface()
        self.spawn_timer = 0

    def spawn_mob(self): # спавнит моба в рандомном месте
        x = random.randint(0, FIELD_WIDTH)
        y = random.randint(0, FIELD_HEIGHT)
        mob = Mob(x, y)
        self.mobs.add(mob)
        self.all_sprites.add(mob)

    def update(self):
        self.player.update()
        for mob in self.mobs:
            mob.update(self.player)

        # Спавн мобов с интервалом
        self.spawn_timer += 1
        if self.spawn_timer > FPS * 2:  # Раз в 2 секунды
            self.spawn_mob()
            self.spawn_timer = 0

    # БОЕВАЯ ЗОНА
    def draw(self):
        screen.fill(BLACK)
        # Рисуем игровую область с рамкой
        pygame.draw.rect(screen, WHITE, (0, 0, FIELD_WIDTH, FIELD_HEIGHT), 5)
        self.all_sprites.draw(screen)
        self.ui.draw(screen)

# Основной цикл
battle = Battle()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    battle.update()
    battle.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

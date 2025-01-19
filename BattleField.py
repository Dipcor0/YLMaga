import pygame
import random
from Constants import UI_HEIGHT, PLAYER_SPEED_MOVE, RED, PLAYER_HP, PLAYER_ARMOR, BLUE, WHITE, SLOT_SIZE, \
    INVENTORY_SLOTS, FPS, GRAY, BLACK

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


# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Sprites/Creatures/персонаж.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 50))  # Изменение размера спрайта персонажа
        self.rect = self.image.get_rect()
        self.rect.center = (FIELD_WIDTH // 2, FIELD_HEIGHT // 2)  # спавн на середине
        self.speed = PLAYER_SPEED_MOVE  # скорость
        self.hp = PLAYER_HP  # здоровье
        self.armor = PLAYER_ARMOR  # броня
        self.dead = False  # флаг смерти игрока
        self.experience = 0  # Заработанный опыт
        self.money = 0  # Заработанные деньги
        self.crystals = 0  # Заработанные кристаллы

    def update(self):  # Кнопки на WASD
        if self.dead:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < FIELD_HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < FIELD_WIDTH:
            self.rect.x += self.speed

    def take_damage(self, damage):
        if self.armor > 0:
            if self.armor >= damage:
                self.armor -= damage  # Броня уменьшается на величину урона, если брони достаточно
            else:
                damage -= self.armor  # Если брони недостаточно, оставшийся урон идет по здоровью
                self.armor = 0  # Броня не может быть отрицательной
        else:
            if damage > 0:
                self.hp -= damage  # Наносим оставшийся урон по здоровью
            if self.hp <= 0:
                self.hp = 0
                self.dead = True

    def add_experience(self, exp):
        self.experience += exp

    def add_money(self, amount):
        self.money += amount

    def add_crystals(self, amount):
        self.crystals += amount


# Моб
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2
        self.damage = 10  # Урон, который наносит моб
        self.attack_timer = 0  # Таймер для периодического нанесения урона
        self.experience = 10  # Опыт за убийство
        self.money = 5  # Деньги за убийство
        self.crystals = 2  # Кристаллы за убийство

    def update(self, target):
        if target.dead:
            return

        if self.rect.colliderect(target.rect):
            self.attack_timer += 1
            if self.attack_timer > FPS * 1:  # Наносим урон каждые 1 секунду
                target.take_damage(self.damage)
                self.attack_timer = 0

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

    def draw(self, surface, player):
        # Рисуем область интерфейса
        pygame.draw.rect(surface, BLUE, (0, FIELD_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))

        # Рисуем текст для здоровья
        hp_text = self.font.render(f"HP: {player.hp}", True, WHITE)
        surface.blit(hp_text, (10, FIELD_HEIGHT + 10))

        # Рисуем текст для брони
        armor_text = self.font.render(f"Armor: {player.armor}", True, WHITE)
        surface.blit(armor_text, (10, FIELD_HEIGHT + 50))

        # Рисуем текст для опыта
        exp_text = self.font.render(f"EXP: {player.experience}", True, WHITE)
        surface.blit(exp_text, (10, FIELD_HEIGHT + 90))

        # Рисуем текст для денег
        money_text = self.font.render(f"Money: {player.money}", True, WHITE)
        surface.blit(money_text, (10, FIELD_HEIGHT + 130))

        # Рисуем текст для кристаллов
        crystals_text = self.font.render(f"Crystals: {player.crystals}", True, WHITE)
        surface.blit(crystals_text, (10, FIELD_HEIGHT + 170))

        exit_text = self.font.render("Esc - выйти из игры", True, WHITE)
        surface.blit(exit_text, (10, FIELD_HEIGHT + 210))

        # GAME OVER
        if player.dead:
            game_over_text = self.font.render("GAME OVER", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

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
        self.mobs = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.ui = Interface()
        self.spawn_timer = 0

    def spawn_mob(self):  # Спавн мобов
        x = random.randint(0, FIELD_WIDTH)
        y = random.randint(0, FIELD_HEIGHT)
        mob = Mob(x, y)
        self.mobs.add(mob)
        self.all_sprites.add(mob)

    def update(self):
        if self.player.dead:
            return  # Если игрок мертв, не обновляем игру

        self.player.update()
        for mob in self.mobs:
            mob.update(self.player)

            # Когда моб умирает, даем опыт, деньги и кристаллы
            if mob.rect.colliderect(self.player.rect) and self.player.hp <= 0:
                self.player.add_experience(mob.experience)
                self.player.add_money(mob.money)
                self.player.add_crystals(mob.crystals)
                mob.kill()  # Убираем моба после его уничтожения

        # Спавн мобов с интервалом
        self.spawn_timer += 1
        if self.spawn_timer > FPS * 2:  # Раз в 2 секунды
            self.spawn_mob()
            self.spawn_timer = 0

    def draw(self):
        if self.player.dead:
            screen.fill(BLACK)  # Чистим экран и рисуем фоновую картинку GAME OVER
        else:
            screen.fill(BLACK)  # Очистка экрана, если игрок живой

        # Рисуем игровую область с рамкой
        pygame.draw.rect(screen, WHITE, (0, 0, FIELD_WIDTH, FIELD_HEIGHT), 5)

        # Отображаем все спрайты (игроков и мобов)
        self.all_sprites.draw(screen)

        # Рисуем интерфейс
        self.ui.draw(screen, self.player)

        # Если игрок мертв, показываем GAME OVER
        if self.player.dead:
            game_over_text = self.ui.font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))


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

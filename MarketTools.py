import Equipment
import pygame
import Constants
from Constants import WHITE, FPS, SIZE_SCREEN, BLUE, SIZE_BOX, DARK_BLUE, DARK_DARK_BLUE, LIGHT_BLUE


class WindowStore:
    def __init__(self):
        self.top = 50
        self.left = 100

        self.font = pygame.font.Font(None, 81)
        self.head1 = self.font.render('Оружие', True, DARK_BLUE)
        self.head1_pos = 20, 10

        self.head2 = self.font.render('Снаряжение', True, DARK_BLUE)
        self.head2_pos = 20, 480
        self.opened = False

        self.items = []
        weapon = [(Equipment.Needles, 10), (Equipment.Fireball, 50), (Equipment.SocialDistance, 100)]
        equipment = [(Equipment.Boots, 150), (Equipment.Breastplate, 250)]

        for index in range(len(weapon)):
            self.items.append(ItemStoreWeapon(*weapon[index],
                                              (self.left + self.head1_pos[0] + (SIZE_BOX[0] + 20) * index,
                                               self.top + self.head1.get_height() + self.head1_pos[1] + 10)))

        for index in range(len(equipment)):
            self.items.append(ItemStoreEquipment(*equipment[index],
                                                 (self.left + self.head2_pos[0] + (SIZE_BOX[0] + 20) * index,
                                                  self.top + self.head2.get_height() + self.head2_pos[1] + 10)))

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
                         (self.left, self.top, SIZE_SCREEN[0] - self.left * 2, SIZE_SCREEN[1] - self.top * 15),
                         width=0)
        screen.blit(self.head1, (self.head1_pos[0] + self.left, self.head1_pos[1] + self.top))
        pygame.draw.rect(screen, BLUE,
                         (self.left, self.top + self.head2_pos[1] - self.head1_pos[1],
                          SIZE_SCREEN[0] - self.left * 2, SIZE_SCREEN[1] - self.top * 15),
                         width=0)
        screen.blit(self.head2, (self.head2_pos[0] + self.left, self.head2_pos[1] + self.top))
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


class ItemStoreEquipment:
    def __init__(self, item, cost, pos):
        self.pos = pos
        self.index_item = Equipment.find_index_equipment(item)
        self.image = pygame.transform.scale(item.image, (30, 30))
        self.name = item.name
        self.text = {'armor': None}
        self.cost = cost

        self.font = pygame.font.Font(None, 30)
        rect_btn = (self.pos[0] + SIZE_BOX[0] // 6,
                    self.pos[1] + SIZE_BOX[1] * 5 // 6 - 10,
                    SIZE_BOX[0] * 4 // 6,
                    SIZE_BOX[1] // 6)
        self.btn = Button(self, f'КУПИТЬ {self.cost}G', Constants.ALL_EQUIPMENT,
                          Constants.PLAYER_EQUIPMENT, self.index_item, rect_btn, cost)

        if self.index_item in Constants.ALL_EQUIPMENT:
            self.btn.not_buying()

        for k, lm in {'armor': (lambda x: x.armor)}.items():
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

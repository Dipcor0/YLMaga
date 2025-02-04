import pygame
from Equipment import *
from Creatures import Player
from Market import Shop
from BattleField import Battle
from Constants import SIZE_SCREEN, load_sprites, FPS

active_scene = 0


class Controller:
    def __enter__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE_SCREEN, pygame.FULLSCREEN)
        load_sprites()

        self.hero = Player()
        self.active_scene = active_scene
        self.scenes = {0: Shop(self.hero),
                       1: Battle(self.hero)}

        self.running = True
        self.clock = pygame.time.Clock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def run(self):
        while self.running:
            scene = self.scenes[self.active_scene]
            if self.active_scene == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        scene.update_all(event)
                        if scene.flag_fight is True:
                            scene.flag_fight = False
                            self.active_scene = 1
                            self.hero.rect.x = SIZE_SCREEN[0] // 2 - self.hero.image.get_width() // 2
                            self.hero.rect.y = SIZE_SCREEN[1] // 2 - self.hero.image.get_height() // 2
                            self.scenes[self.active_scene].reboot()

            elif self.active_scene == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        self.active_scene = 0
                        self.hero.rect.x = SIZE_SCREEN[0] // 2 - self.hero.image.get_width() // 2
                        self.hero.rect.y = SIZE_SCREEN[1] // 2 - self.hero.image.get_height() // 2


            scene.update_all()
            scene.draw_all(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)


with Controller() as game:
    game.run()

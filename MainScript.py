import pygame
from Equipment import *
from Scenes import Shop, Battle
from Creatures import Hero
from Constants import SIZE_SCREEN, load_sprites, GROUP_PLAYER

active_scene = 0


class Controller:
    def __enter__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE_SCREEN, pygame.FULLSCREEN)
        load_sprites()

        self.hero = Hero()
        self.scenes = {0: Shop(self.hero),
                       1: Battle(self.hero)}

        self.running = True
        self.clock = pygame.time.Clock()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def run(self):
        while self.running:
            scene = self.scenes[active_scene]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    self.hero.update(event)
                    scene.update(event)
                # добавление нужных обработчиков
                # if event.type == pygame.MOUSEMOTION:
                #     scene.update(event)
                # по типу вот этого

            scene.update()
            scene.draw(self.screen)
            pygame.display.flip()


with Controller() as game:
    game.run()

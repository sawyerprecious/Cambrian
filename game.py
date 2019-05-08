import pygame
import os
import creature
import random


class Game:

    def __init__(self):
        self.width = 1200
        self.height = 750
        self.win = pygame.display.set_mode((self.width, self.height))
        self.creatures = []
        self.food_items = []
        self.bg = pygame.image.load(os.path.join("assets", "background.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.create_food()

    def run(self):
        run = True

        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    c = creature.Creature(pos, 15)
                    self.creatures.append(c)

            for c in self.creatures:
                c.draw(self.win)

            self.draw()

        pygame.quit()

    def draw(self):
        self.win.blit(self.bg, (0, 0))
        for c in self.creatures:
            c.friction()
            pygame.draw.circle(self.win, (255, 0, 0), (int(getattr(c, "position").x), int(getattr(c, "position").y)), 15, 0)
            for f in self.food_items:
                if c.collide(f[0], f[1]):
                    self.food_items.remove(f)
        for f in self.food_items:
            pygame.draw.circle(self.win, (0, 255, 0), (f[0], f[1]), 5, 0)
        pygame.display.update()

    def create_food(self):
        i = 0

        while i < 100:
            self.food_items.append((random.randint(50, 1150), random.randint(50, 700)))
            i += 1


g = Game()
g.run()

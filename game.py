import pygame
import os
import creature
import random
import math
import pygame.freetype


class Game:

    def __init__(self):

        pygame.init()

        self.width = 1200
        self.height = 750
        self.win = pygame.display.set_mode((self.width, self.height))
        self.creatures = []
        self.food_items = []
        self.bubbles = []
        self.bg = pygame.image.load(os.path.join("assets", "background.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.create_food()
        self.create_creatures()

    def run(self):

        run = True
        pause = False
        tick = 0

        clock = pygame.time.Clock()

        while run:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] < 30 and pygame.mouse.get_pos()[1] < 30:
                        pause = not pause

            if not pause:
                for c in self.creatures:
                    c.draw(self.win)

                self.draw_game()
                self.draw_pause_button(not pause)
            else:
                tick += 1
                if tick > 60:
                    tick = 0
                self.draw_pause_menu()
                self.draw_pause_button(tick > 30)

        pygame.quit()

    def draw_game(self):

        self.win.blit(self.bg, (0, 0))

        to_remove_bubbles = []

        bub = pygame.image.load(os.path.join("assets", "bubble.png"))
        bub.convert()

        for b in self.bubbles:
            r = random.randint(0, 5)
            if r == 0:
                to_remove_bubbles.append(b)

            else:
                self.win.blit(bub, (b[0], b[1]))

        self.bubbles = [i for i in self.bubbles if i not in to_remove_bubbles]

        mouths = []
        damage_parts = []

        to_remove_creatures = []

        for c in self.creatures:
            if not getattr(c, "home"):
                mouths.append(getattr(c, "parts")[0])
                damage_parts = damage_parts + (getattr(c, "dmg_parts"))

        for c in self.creatures:
            for d in damage_parts:
                if (not c == getattr(d, "owner"))\
                        and (not getattr(c, "home"))\
                        and c.collide(d.true_position_dmg()[0], d.true_position_dmg()[1]):

                    if getattr(c, "health") > 0:
                        setattr(c, "health", getattr(c, "health") - 1)
                        setattr(c, "dmg", True)
                        ang = math.atan2(getattr(c, "position")[1] - d.true_position()[1],
                                         getattr(c, "position")[0] - d.true_position()[0])
                        ang_vec = (math.cos(ang) * max(0.5, getattr(d, "owner").vel[0]),
                                   -math.sin(ang) * max(0.5, getattr(d, "owner").vel[1]))
                        setattr(c, "vel", getattr(c, "vel") + ang_vec)

            if not getattr(c, "home"):
                for i in range(max(1, int(c.size / 3))):
                    r = random.randint(0, c.size)
                    r2 = random.randint(0, c.size)
                    self.bubbles.append((int(getattr(c, "position")[0] + r - c.size / 2),
                                         int(getattr(c, "position")[1] + r2 - c.size / 2)))

            if getattr(c, "health") <= 0:
                to_remove_creatures.append(c)
                for i in range(max(1, int(c.size / 3))):
                    r = random.randint(0, 25)
                    r2 = random.randint(0, 25)
                    self.food_items.append((int(getattr(c, "position")[0] + r - 12.5),
                                            int(getattr(c, "position")[1] + r2 - 12.5)))

            if not to_remove_creatures.__contains__(c):
                getattr(c, "brain").get_closest_things(self.creatures, self.food_items)
                c.draw(self.win)
                setattr(c, "dmg", False)

        self.creatures = [i for i in self.creatures if i not in to_remove_creatures]

        to_remove_food = []

        for f in self.food_items:
            for mouth in mouths:
                if mouth.check_collision(f[0], f[1]):
                    mouth.next_in_animation()
                    to_remove_food.append(f)

                else:
                    pygame.draw.circle(self.win, (0, 255, 0), (f[0], f[1]), 5, 0)

        self.food_items = [i for i in self.food_items if i not in to_remove_food]

    def draw_pause_button(self, p):
        self.win.blit(pygame.image.load(os.path.join("assets",
                                                     "pause-button.png" if p else "play-button.png")), (5, 5))
        pygame.display.update()

    def draw_pause_menu(self):
        pygame.draw.rect(self.win, (255, 255, 255), pygame.rect.Rect(500, 300, 200, 30))
        large_text = pygame.font.Font('freesansbold.ttf', 30)
        text_surf, text_rect = large_text.render("Paused", True, (0, 0, 0)),\
                               large_text.render("Paused", True, (0, 0, 0)).get_rect()
        text_rect.center = (600, 315)
        self.win.blit(text_surf, text_rect)

        pygame.display.update()
        # TODO: finish the actual menu; maybe stuff like quit, see stats, etc.

    def create_food(self):
        i = 0

        while i < 100:
            self.food_items.append((random.randint(50, 1150), random.randint(50, 700)))
            i += 1

    def create_creatures(self):
        positions = []
        i = 0

        while i < 10:
            r = random.randint(0, 3895)
            r2 = random.randint(5, 25)

            if r <= 1198:
                pos = (r + 1, 0)
            elif r <= 1947:
                pos = (1199, r - 1198)
            elif r <= 3146:
                pos = (r - 1947, 749)
            elif r < 3896:
                pos = (0, r - 3146)

            c = creature.Creature(pos, r2, None)
            flag = False
            for p in positions:
                if r - 50 < p < r + 50:
                    flag = True
            if not flag:
                positions.append(r)
                self.creatures.append(c)
            else:
                i -= 1

            i += 1


g = Game()
g.run()

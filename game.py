import pygame
import os
import creature
import random
import math
import pygame.freetype
import operator
import threading
import copy


class Game:

    def __init__(self):
        self.lock = threading.Lock()

        pygame.init()
        self.creatures = []
        self.food_items = []
        self.bubbles = []
        self.bg = None
        self.gen_num = 0
        self.run_num = 0
        self.gene_pool = []
        self.width = 1200
        self.height = 750
        self.win = pygame.display.set_mode((self.width, self.height))
        self.select_creatures()
        self.set_up_gen()
        self.best_from_last_gen = None

    def set_up_gen(self):
        self.creatures = []
        self.food_items = []
        self.bubbles = []
        self.bg = pygame.image.load(os.path.join("assets", "background.png")).convert()
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.create_food()
        self.create_creatures()
        self.run_num += 1

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
                    pos = pygame.mouse.get_pos()
                    if pos[0] < 30 and pos[1] < 30:
                        pause = not pause
                        tick = 0
                    if pause and 310 < pos[1] < 340 and 550 < pos[0] < 650:
                        run = False

            if not pause:
                for c in self.creatures:
                    c.draw(self.win)

                self.draw_game()
                self.draw_pause_button(not pause)
            else:
                if tick is 0:
                    self.draw_pause_menu_background()
                    self.draw_pause_menu_contents()
                tick += 1
                if tick > 60:
                    tick = 1
                self.draw_pause_button(tick > 30)

        pygame.quit()

    def draw_game(self):
        self.lock.acquire()
        self.win.blit(self.bg, (0, 0))

        to_remove_bubbles = []

        bub = pygame.image.load(os.path.join("assets", "bubble.png")).convert_alpha()
        bub.convert()

        for b in self.bubbles:
            r = random.randint(0, 5)
            if r == 0:
                to_remove_bubbles.append(b)

            else:
                self.win.blit(bub, (b[0], b[1]))

        self.lock.release()

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
                if (not c == getattr(d, "owner") and d.type is not "eye")\
                        and (not getattr(c, "home"))\
                        and c.collide(d.true_position_dmg()[0], d.true_position_dmg()[1], d.size):

                    if getattr(c, "health") > 0:
                        setattr(c, "health", getattr(c, "health") - int(getattr(d, "owner").size / 3))
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
                    setattr(mouth.owner, "food_collected", getattr(mouth.owner, "food_collected") + 1)
                    to_remove_food.append(f)

                else:
                    self.lock.acquire()
                    pygame.draw.circle(self.win, (0, 255, 0), (f[0], f[1]), 5, 0)
                    self.lock.release()

        self.food_items = [i for i in self.food_items if i not in to_remove_food]

        flag = True
        for c in self.creatures:
            if not getattr(c, "home"):
                flag = False
                break
        if flag:
            self.next_run()

    def next_run(self):
        if self.run_num < 10:
            self.set_up_gen()
        else:
            self.gen_num += 1
            self.run_num = 0
            self.select_creatures()

    def draw_pause_button(self, p):
        self.lock.acquire()
        self.win.blit(pygame.image.load(os.path.join("assets",
                                                     "pause-button.png" if p
                                                     else "play-button.png")).convert(), (5, 5))
        pygame.display.update()
        self.lock.release()

    def draw_pause_menu_background(self):
        s = pygame.Surface((300, 300))
        s.set_alpha(90)
        s.fill((0, 0, 0))
        self.lock.acquire()
        self.win.blit(s, (450, 225))
        self.lock.release()

    def draw_pause_menu_contents(self):
        self.lock.acquire()
        pygame.draw.rect(self.win, (255, 255, 255), pygame.rect.Rect(500, 260, 200, 30))
        large_text = pygame.font.Font('freesansbold.ttf', 30)
        text_surf, text_rect = large_text.render("Paused", True, (0, 0, 0)),\
                               large_text.render("Paused", True, (0, 0, 0)).get_rect()
        text_rect.center = (600, 275)
        self.win.blit(text_surf, text_rect)

        pygame.draw.rect(self.win, (255, 255, 255), pygame.rect.Rect(550, 310, 100, 30))
        large_text = pygame.font.Font('freesansbold.ttf', 30)
        text_surf, text_rect = large_text.render("Quit", True, (255, 0, 0)), \
                               large_text.render("Quit", True, (255, 0, 0)).get_rect()
        text_rect.center = (600, 325)
        self.win.blit(text_surf, text_rect)

        self.lock.release()
        self.draw_best()
        self.lock.acquire()

        pygame.display.update()
        self.lock.release()

    def draw_best(self):
        bflg = self.best_from_last_gen
        if not isinstance(bflg, type(None)):
            self.lock.acquire()
            pygame.draw.rect(self.win, (255, 255, 255), pygame.rect.Rect(500, 385, 200, 112))
            large_text = pygame.font.Font('freesansbold.ttf', 24)
            text_surf, text_rect = large_text.render("Best of last gen:", True, (0, 0, 0)), \
                                   large_text.render("Best of last gen:", True, (0, 0, 0)).get_rect()
            text_rect.center = (600, 402)
            self.win.blit(text_surf, text_rect)
            self.lock.release()

            c = creature.Creature((600, 440), bflg, self.lock, True)

            for p in c.parts:
                p.determine_rotation(True)

            c.draw(self.win, False)

            # TODO: show stats like number in species (future)

            self.lock.acquire()

            mid_text = pygame.font.Font('freesansbold.ttf', 13)
            text_surf, text_rect = mid_text.render("Fitness: " + str(int(getattr(bflg, "fitness"))),
                                                   True, (0, 0, 0)),\
                                   mid_text.render("Fitness: " + str(int(getattr(bflg, "fitness"))),
                                                   True, (0, 0, 0)).get_rect()
            text_rect.center = (540, 450)
            self.win.blit(text_surf, text_rect)

            self.lock.release()

        self.lock.acquire()
        mid_text = pygame.font.Font('freesansbold.ttf', 18)
        text_surf, text_rect = mid_text.render("Gen# " + str(self.gen_num + 1) + ", Run# " + str(self.run_num),
                                                 True, (255, 255, 255)), \
                               mid_text.render("Gen# " + str(self.gen_num + 1) + ", Run# " + str(self.run_num),
                                                 True, (255, 255, 255)).get_rect()
        text_rect.center = (520, 512)
        self.win.blit(text_surf, text_rect)
        self.lock.release()

    def create_food(self):
        i = 0

        while i < 100:
            self.food_items.append((random.randint(50, 1150), random.randint(50, 700)))
            i += 1

    def create_creatures(self):
        positions = []
        i = 0
        genes_this_run = self.gene_pool[self.run_num * 10:self.run_num * 10 + 10]
        new_genes = []

        while i < 10:
            r = random.randint(0, 3895)
            pos = 0

            if r <= 1198:
                pos = (r + 1, 0)
            elif r <= 1947:
                pos = (1199, r - 1198)
            elif r <= 3146:
                pos = (r - 1947, 749)
            elif r < 3896:
                pos = (0, r - 3146)

            c = creature.Creature(pos, genes_this_run[i], self.lock)

            flag = False
            for p in positions:
                if r - 50 < p < r + 50:
                    flag = True
            if not flag:
                positions.append(r)
                self.creatures.append(c)
                new_genes.append(c.genes)
            else:
                i -= 1

            i += 1

        self.gene_pool[self.run_num * 10:self.run_num * 10 + 10] = new_genes

    def select_creatures(self):
        if self.gene_pool.__len__() is not 0:
            self.gene_pool.sort(key=operator.attrgetter('fitness'), reverse=True)
            self.best_from_last_gen = copy.deepcopy(self.gene_pool[0])
            total_fitness = 0
            for gene in self.gene_pool:
                total_fitness += gene.fitness
            new_pool = []
            for i in range(100):
                flag = True
                r = random.randint(0, int(total_fitness))
                k = 0
                tsf = 0

                while flag:
                    if tsf + self.gene_pool[k].fitness >= r:
                        flag = False
                        new_pool.append(self.gene_pool[k])
                    else:
                        tsf += self.gene_pool[k].fitness
                        k += 1

            self.gene_pool = new_pool
        else:
            for i in range(100):
                self.gene_pool.append(None)


g = Game()
g.run()

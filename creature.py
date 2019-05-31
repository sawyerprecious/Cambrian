import pygame
import math
import body_part
import os
import brain
import genome

vec = pygame.math.Vector2


class Creature:

    def __init__(self, pos, genes, lock, copy=False):
        self.lock = lock

        self.genes = genome.Genome(genes, copy)
        self.size = self.genes.body_nodes.get(0).size
        self.health = 2 * self.size
        self.energy = 250000
        self.food_collected = 0
        self.dmg = False

        self.vel = vec(0, 0)
        num_flag = 1
        for node in self.genes.body_nodes.values():
            if node.part_type is "flagella":
                num_flag += 1
        self.acceleration = vec(0, -0.2 * (1 + 0.05 * num_flag) + ((self.size - 15) / 100))
        self.position = vec(pos[0], pos[1])
        self.angle_speed = 0
        self.angle = self.set_angle()
        self.acceleration.rotate_ip(self.angle)

        self.img = pygame.image.load(os.path.join("assets", "gradient.png")).convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.size * 2 + 1, self.size * 2 + 1))
        self.home = False

        self.parts = []
        self.animated_parts = []
        self.dmg_parts = []
        self.setup_parts()

        self.brain = brain.Brain(self)

    def setup_parts(self):
        mouth = body_part.BodyPart(0, self.size / 1.5, self.size, self, "mouth", self.lock)
        self.parts.append(mouth)

        eye = body_part.BodyPart(0, 0, self.size / 3, self, "eye", self.lock)
        self.parts.append(eye)

        flag = body_part.BodyPart(180, 0, self.size * 1.5, self, "flagella", self.lock)
        self.parts.append(flag)

        for gene in self.genes.body_nodes.values():
            if gene.part_type is not "body":
                to_add = body_part.BodyPart(gene.angle, gene.size, gene.position, self, gene.part_type, self.lock)
                self.parts.append(to_add)

        for part in self.parts:
            if part.type is "spike" or part.type is "mouth" or part.name is "stalk-eye":
                self.dmg_parts.append(part)
            elif part.type is "flagella":
                self.animated_parts.append(part)

    def set_angle(self):
        centre = (600, 325)
        return math.degrees(math.atan2(self.position[1] - centre[1], self.position[0] - centre[0])) - 90

    def friction(self):
        self.vel.x = self.vel.x - (self.vel.x / (10 + self.size / 2))
        self.vel.y = self.vel.y - (self.vel.y / (10 + self.size / 2))

    def draw(self, win, go=True):
        # draws creature

        self.friction()

        colour1 = self.genes.body_nodes.get(0).strength
        colour2 = self.genes.body_nodes.get(0).position
        colour3 = self.genes.body_nodes.get(0).angle

        self.lock.acquire()
        pygame.draw.circle(win,
                           (max(0, colour1 - 1),
                            max(0, colour2 - 1),
                            max(0, colour3 - 1)) if self.dmg is False else (255, 0, 0),
                           (int(self.position.x), int(self.position.y)), self.size, 0)
        win.blit(self.img, (int(self.position.x - self.size - 1), int(self.position.y - self.size - 1)))
        self.lock.release()

        for part in self.parts:
            part.draw(win)

        if go:
            self.move()

    def collide(self, x, y, d):
        # checks collision
        if self.position.x + self.size >= x - d / 3 and x + d / 3 >= self.position.x - self.size:
            if self.position.y + self.size >= y - d / 3 and y + d / 3 >= self.position.y - self.size:
                return True
        return False

    def front_pos(self):
        fpx = self.position.x + (self.size * math.sin(math.radians(self.angle)))
        fpy = self.position.y - (self.size * math.cos(math.radians(self.angle)))

        return fpx, fpy

    def move(self):
        # moves creature

        if not self.home:
            # keys = pygame.key.get_pressed()
            dec = self.brain.decide()
            flag_rotation = False
            flag_animation = False
            # if keys[pygame.K_LEFT]:
            if dec.__contains__(2):
                self.energy -= self.size
                self.angle_speed = -3
                flag_animation = True
                flag_rotation = True
            # if keys[pygame.K_RIGHT]:
            if dec.__contains__(3):
                self.energy -= self.size
                self.angle_speed = 3
                flag_animation = True
                flag_rotation = True
            # If up or down is pressed, accelerate by
            # adding the acceleration to the velocity vector.
            # if keys[pygame.K_UP]:
            if dec.__contains__(1):
                self.energy -= self.size ** 2 + len(self.animated_parts) * 4
                self.vel += self.acceleration
                flag_animation = True
            # if keys[pygame.K_DOWN]:
            if dec.__contains__(4):
                self.energy -= self.size ** 2 + len(self.animated_parts) * 4
                self.vel -= self.acceleration
                flag_animation = True

            if flag_animation:
                self.animate_parts()
            if flag_rotation:
                self.rotate()

            self.position += self.vel

            if self.energy <= 0:
                self.health = 0

            if self.position.x < 0 or self.position.x > 1200 or self.position.y < 0 or self.position.y > 750:
                self.position.x = max(self.position.x, 0)
                self.position.y = max(self.position.y, 0)
                self.position.x = min(self.position.x, 1200)
                self.position.y = min(self.position.y, 750)
                self.got_home()

    def animate_parts(self):
        for part in self.animated_parts:
            part.next_in_animation()

    def rotate(self):
        # Rotate the acceleration vector
        self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        for part in self.dmg_parts:
            part.determine_rotation(True)

    def got_home(self):
        self.vel = vec(0, 0)
        self.home = True
        self.genes.fitness = self.determine_fitness()

    def determine_fitness(self):
        if self.food_collected is 0:
            fit = 0
        else:
            fit = self.food_collected ** 2 + 2 * (self.energy / 250000) + self.health / self.size
        return fit


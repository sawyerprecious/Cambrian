import pygame
import math
import body_part

vec = pygame.math.Vector2


class Creature:

    def __init__(self, pos, size, genes):

        self.genes = genes
        self.size = size    # TODO: remove size from init, based on genes
        self.health = 2 * self.size
        self.energy = 15000
        self.food_collected = 0
        self.dmg = False

        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2 + ((self.size - 15) / 100))
        self.position = vec(pos[0], pos[1])
        self.angle_speed = 0
        self.angle = self.set_angle()
        self.acceleration.rotate_ip(self.angle)

        self.img = None     # TODO: some basic image for all creatures
        self.home = False

        self.parts = []
        self.setup_parts()

    def setup_parts(self):
        # TODO: use the genome to determine this
        mouth = body_part.BodyPart(0, self.size / 1.5, self.size, self, "mouth")
        self.parts.append(mouth)

        spike = body_part.BodyPart(40, self.size / 3, self.size + 5, self, "spike")
        spike2 = body_part.BodyPart(320, self.size / 3, self.size + 5, self, "spike")
        self.parts.append(spike)
        self.parts.append(spike2)

    def set_angle(self):
        centre = (600, 325)
        return math.degrees(math.atan2(self.position[1] - centre[1], self.position[0] - centre[0])) - 90

    def friction(self):
        self.vel.x = self.vel.x - (self.vel.x / (self.size * 2))
        self.vel.y = self.vel.y - (self.vel.y / (self.size * 2))

    def draw(self, win):
        # draws creature

        self.friction()

        pygame.draw.circle(win, (255, 255, 255) if self.dmg is False else (255, 0, 0), (int(self.position.x), int(self.position.y)), self.size, 0)

        for part in self.parts:
            part.draw(win)

        self.move()

    def collide(self, x, y):
        # checks collision
        if self.position.x + self.size >= x >= self.position.x - self.size:
            if self.position.y + self.size >= y >= self.position.y - self.size:
                return True
        return False

    def body_part_collision(self, x, y):
        for part in self.parts:
            if part.check_collision(x, y):
                return True
        return False

    def front_pos(self):
        fpx = self.position.x + (self.size * math.sin(math.radians(self.angle)))
        fpy = self.position.y - (self.size * math.cos(math.radians(self.angle)))

        return fpx, fpy

    def move(self):
        # moves creature

        if not self.home:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.energy -= self.size  # TODO: based on size and other factors
                self.angle_speed = -4
                self.rotate()
            if keys[pygame.K_RIGHT]:
                self.energy -= self.size  # TODO: based on size and other factors
                self.angle_speed = 4
                self.rotate()
            # If up or down is pressed, accelerate by
            # adding the acceleration to the velocity vector.
            if keys[pygame.K_UP]:
                self.energy -= self.size  # TODO: based on size and other factors
                self.vel += self.acceleration
            if keys[pygame.K_DOWN]:
                self.energy -= self.size  # TODO: based on size and other factors
                self.vel -= self.acceleration

            self.position += self.vel

            if self.energy <= 0:
                self.health = 0

            if self.position.x < 0 or self.position.x > 1200 or self.position.y < 0 or self.position.y > 750:
                self.position.x = max(self.position.x, 0)
                self.position.y = max(self.position.y, 0)
                self.position.x = min(self.position.x, 1200)
                self.position.y = min(self.position.y, 750)
                self.got_home()

    def rotate(self):
        # Rotate the acceleration vector
        self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            return True
        else:
            return False

    def got_home(self):
        self.front_pos()
        self.vel = vec(0, 0)
        self.home = True
        # if self.food_collected == 0:
        #     # die
        # else:
        #     # reproduction


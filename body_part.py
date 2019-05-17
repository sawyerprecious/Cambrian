import math
import pygame


class BodyPart:

    def __init__(self, angle, size, position, owner, type):
        self.angle = angle
        self.size = size
        self.position = position
        self.owner = owner
        self.type = type

    def check_collision(self, x, y):
        fpx = self.true_position()[0]
        fpy = self.true_position()[1]

        if fpx + self.size >= x >= fpx - self.size:
            if fpy + self.size >= y >= fpy - self.size:
                return True
        return False

    def draw(self, win):
        fpx = self.true_position()[0]
        fpy = self.true_position()[1]

        pygame.draw.circle(win, (0, 0, 250 if self.type == "spike" else 0), (int(fpx), int(fpy)), 2, 0)

    def true_position(self):
        op = getattr(self.owner, "position")

        fpx = op.x + (self.position * math.sin(math.radians(getattr(self.owner, "angle") + self.angle)))
        fpy = op.y - (self.position * math.cos(math.radians(getattr(self.owner, "angle") + self.angle)))

        return fpx, fpy

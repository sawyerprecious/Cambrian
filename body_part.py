import math
import pygame
import os


class BodyPart:

    def __init__(self, angle, size, position, owner, part_type):
        self.img = None
        self.angle = angle
        self.size = size
        self.position = position
        self.owner = owner
        self.type = part_type
        self.determine_rotation()

    def check_collision(self, x, y):
        fpx = self.true_position_dmg()[0]
        fpy = self.true_position_dmg()[1]

        if fpx + self.size >= x >= fpx - self.size:
            if fpy + self.size >= y >= fpy - self.size:
                return True
        return False

    def draw(self, win):
        fpx = self.true_position()[0]
        fpy = self.true_position()[1]

        fpdx = self.true_position_dmg()[0]
        fpdy = self.true_position_dmg()[1]

        win.blit(self.img, (int(fpx - self.img.get_width() / 2), int(fpy - self.img.get_height() / 2)))

        pygame.draw.circle(win, (255, 0, 0), (int(fpdx), int(fpdy)), 2, 0)

    def true_position(self):
        op = getattr(self.owner, "position")

        fpx = op.x + (self.position * math.sin(math.radians(getattr(self.owner, "angle") + self.angle)))
        fpy = op.y - (self.position * math.cos(math.radians(getattr(self.owner, "angle") + self.angle)))

        return fpx, fpy

    def true_position_dmg(self):
        op = getattr(self.owner, "position")

        fpx = op.x + (self.position * 1.5 * math.sin(math.radians(getattr(self.owner, "angle") + self.angle)))
        fpy = op.y - (self.position * 1.5 * math.cos(math.radians(getattr(self.owner, "angle") + self.angle)))

        return fpx, fpy

    def determine_rotation(self):
        self.img = pygame.image.load(os.path.join("assets", self.type + ".png"))
        self.img = pygame.transform.scale(self.img, (int(self.position) if self.type is "eye" or self.type is "mouth"
                                                     else int(self.position / 2),
                                                     int(self.position)))
        self.img = pygame.transform.rotate(self.img, 360 - getattr(self.owner, "angle") - self.angle)

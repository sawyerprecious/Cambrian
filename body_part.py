import math
import pygame
import os
import random
import copy


class BodyPart:

    def __init__(self, angle, size, position, owner, part_type, lock):
        self.lock = lock
        self.img = None
        self.angle = angle
        self.size = size
        self.position = position
        self.owner = owner
        self.type = part_type
        self.state = self.set_state()
        self.name = self.set_name()
        self.determine_rotation(False)

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

        if self.type is "mouth" and self.state > 1:
            self.next_in_animation()

        self.lock.acquire()
        win.blit(self.img, (int(fpx - self.img.get_width() / 2), int(fpy - self.img.get_height() / 2)))
        self.lock.release()

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

    def determine_rotation(self, flag):
        self.img = pygame.image.load(os.path.join("assets", self.name + ".png")).convert_alpha()
        if self.type is "eye":
            if self.name is "eye":
                size = (int(self.position * 3), int(self.position * 3))
            else:
                size = (int(self.position * (5 / 6)), int(self.position))
        elif self.type is "mouth":
            size = (int(self.position), int(self.position))
        elif self.type is "spike":
            size = (int(self.position / 2), int(self.position))
        elif self.type is "flagella":
            size = (int(self.position / 2), int(self.position))
        else:
            size = (int(self.position), int(self.position))

        self.lock.acquire()
        self.img = pygame.transform.scale(self.img, size).convert_alpha()
        self.lock.release()
        if flag:
            angle = getattr(self.owner, "angle")
            if isinstance(angle, (int, float)) and size[0] > 0 and size[1] > 0:
                self.lock.acquire()
                self.img = pygame.transform.rotate(self.img, 360 - max(0, angle) - self.angle).convert_alpha()
                self.lock.release()
            else:
                print("rip.  No rotation allowed :(")

    def set_state(self):
        if self.type is "flagella":
            return random.randint(1, 14)
        else:
            return 1

    def set_name(self):
        if self.type is "mouth" or self.type is "flagella":
            return self.type + str(self.state)
        elif self.type is "eye" and self.position > self.owner.size * 0.8:
            self.owner.dmg_parts.append(self)
            self.position = int((1 + (self.owner.size - self.position) * .1) * self.owner.size)
            return "stalk-eye"
        else:
            return self.type

    def next_in_animation(self):
        if self.type is "flagella":
            self.state += .23
            if self.state > 14.48:
                self.state = 1
            former_name = copy.deepcopy(self.name)
            self.name = "flagella" + str(int(self.state))
            if former_name != self.name:
                self.determine_rotation(True)
        elif self.type is "mouth":
            self.state += .1
            if self.state > 2:
                self.state = 1
            former_name = copy.deepcopy(self.name)
            self.name = "mouth" + str(1 if self.state is 1 else 2)
            if former_name != self.name:
                self.determine_rotation(True)
        else:
            self.determine_rotation(True)

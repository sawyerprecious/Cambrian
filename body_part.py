import math


class BodyPart:

    def __init__(self, angle, size, position, owner):
        self.angle = angle
        self.size = size
        self.position = position
        self.owner = owner

    def check_collision(self, x, y):
        op = getattr(self.owner, "position")

        fpx = op.x + (self.position * math.sin(math.radians(getattr(self.owner, "angle") + self.angle)))
        fpy = op.y - (self.position * math.cos(math.radians(getattr(self.owner, "angle") + self.angle)))

        if fpx + self.size >= x >= fpx - self.size:
            if fpy + self.size >= y >= fpy - self.size:
                return True
        return False

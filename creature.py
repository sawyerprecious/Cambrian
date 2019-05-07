import pygame

class Creature:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.health = 0
        self.img = None

    def draw(self, win):
        # draws creature
        win.blit(self.img, (self.x, self.y))
        self.move()
        pass

    def collide(self, x, y):
        # checks collision
        if x <= self.x + self.size and x >= self.x:
            if y <= self.y + self.size and y >= self.y:
                return True
        return False

    def move(self):
        # moves creature
        pass

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            return True
        else:
            return False



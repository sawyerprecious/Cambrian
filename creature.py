import pygame

vec = pygame.math.Vector2


class Creature:

    def __init__(self, pos, size):
        self.size = size
        self.health = 0
        self.energy = 0
        self.foodCollected = 0
        self.img = None
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2)
        self.angle_speed = 0
        self.angle = 0  # TODO: point to center of screen
        self.position = vec(pos[0], pos[1])
        self.home = False

    def friction(self):
        self.vel.x = self.vel.x - (self.vel.x / 30)
        self.vel.y = self.vel.y - (self.vel.y / 30)

    def draw(self, win):
        # draws creature
        # win.blit(self.img, (self.x, self.y))
        # pygame.draw.circle(win, (0, 0, 255), (int(self.position.x), int(self.position.y)), 5, 0)
        # pygame.display.update()
        self.move()

    def collide(self, x, y):
        # checks collision
        if self.position.x + self.size >= x >= self.position.x - self.size:
            if self.position.y + self.size >= y >= self.position.y - self.size:
                return True
        return False

    def move(self):
        # moves creature

        if not self.home:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.angle_speed = -4
                self.rotate()
            if keys[pygame.K_RIGHT]:
                self.angle_speed = 4
                self.rotate()
            # If up or down is pressed, accelerate by
            # adding the acceleration to the velocity vector.
            if keys[pygame.K_UP]:
                self.vel += self.acceleration
            if keys[pygame.K_DOWN]:
                self.vel -= self.acceleration

            self.position += self.vel

            if self.position.x < 0 or self.position.x > 1200 or self.position.y < 0 or self.position.y > 750:
                self.position.x = max(self.position.x, 0)
                self.position.y = max(self.position.y, 0)
                self.position.x = min(self.position.x, 1200)
                self.position.y = min(self.position.y, 750)
                self.got_home()

    def rotate(self):
        # Rotate the acceleration vector.
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
        self.vel = vec(0, 0)
        self.home = True
        # if self.foodCollected == 0:
        #     # die
        # else:
        #     # reproduction
        pass


import math


class Brain:

    def __init__(self, creature):

        self.creature = creature

        self.closest_food_dist = 5000
        self.closest_food_angle = 0

        self.closest_creature_dist = 5000
        self.closest_creature_angle = 0

        self.closest_wall_dist = 1
        self.closest_wall_angle = 180

    def decide(self):
        to_return = []
        if self.closest_food_angle < 170:
            to_return.append(2)
        elif self.closest_food_angle > 190:
            to_return.append(4)
        else:
            to_return.append(1)
        to_return.append(0)     # TODO: replace with actual decision making
        return to_return

    def get_closest_things(self, creatures, food):

        wall_x = 0 if self.creature.position.x <= 600 else 1200
        wall_y = 0 if self.creature.position.y <= 325 else 750
        dist_wall_x = abs(wall_x - self.creature.position.x)
        dist_wall_y = abs(wall_y - self.creature.position.y)
        self.closest_wall_dist = min(dist_wall_x, dist_wall_y)
        x_is_less = dist_wall_x < dist_wall_y
        cw = (wall_x if x_is_less else self.creature.position.x, wall_y if not x_is_less else self.creature.position.y)
        self.closest_wall_angle = math.degrees(math.atan2(self.creature.position.y - cw[1],
                                                          self.creature.position.x - cw[0])) + 90

        closest_food = 5000
        cf = (0, 0)
        for f in food:
            hyp = math.hypot(f[0] - self.creature.position.x, f[1] - self.creature.position.y)
            if closest_food > hyp:
                cf = f
                closest_food = hyp
        cf_angle = math.degrees(math.atan2(self.creature.position.y - cf[1],
                                           self.creature.position.x - cf[0])) + 90

        if len(food) is 0:
            cf_angle = self.closest_wall_angle

        self.closest_food_dist = closest_food
        self.closest_food_angle = (cf_angle - self.creature.angle) % 360 if cf_angle >= 0\
            else (360 + cf_angle - self.creature.angle) % 360

        closest_creature = 5000
        cc_angle = 0
        for c in creatures:
            closest_creature = min(closest_creature, math.hypot(getattr(c, "position").x - self.creature.position.x,
                                                                getattr(c, "position").y - self.creature.position.y))
            cc_angle = math.degrees(math.atan2(self.creature.position.y - getattr(c, "position").y,
                                               self.creature.position.x - getattr(c, "position").x)) + 90
        self.closest_creature_dist = closest_creature
        self.closest_creature_angle = (cc_angle - self.creature.angle) % 360 if cc_angle >= 0\
            else (360 + cf_angle - self.creature.angle) % 360

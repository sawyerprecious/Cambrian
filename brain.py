import math


class Brain:

    def __init__(self, creature):

        self.time_since_last_move = 0

        self.creature = creature

        self.neurons = creature.genes.brain_nodes

        self.closest_food_dist = 5000
        self.closest_food_angle = 0

        self.closest_creature_dist = 5000
        self.closest_creature_angle = 0

        self.closest_wall_dist = 1
        self.closest_wall_angle = 180

    def decide(self):
        self.observe_surroundings()
        to_return = []
        for i in range(1, 4):
            if self.neurons.get(14 + i).val > 0:
                to_return.append(i)
        # Simple AI:
        # to_return = []
        # if self.closest_food_angle < 170:
        #     to_return.append(2)
        # elif self.closest_food_angle > 190:
        #     to_return.append(4)
        # else:
        #     to_return.append(1)

        if to_return.__contains__(1):
            self.time_since_last_move = 0
        else:
            self.time_since_last_move += 1
            if self.time_since_last_move > 100:
                self.creature.health = 0

        self.reset_brain()
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

    def observe_surroundings(self):
        for neuron in self.neurons.values():
            if neuron.node_type is "input":
                if neuron.id is 0:                                                  #   Energy
                    neuron.val = self.creature.energy / 250000
                    neuron.pass_to_outgoing()
                elif neuron.id is 1:                                                #   Health
                    neuron.val = self.creature.health / (2 * self.creature.size)
                    neuron.pass_to_outgoing()
                elif neuron.id is 2:                                                #   Food dist
                    neuron.val = self.closest_food_dist / 1416
                    neuron.pass_to_outgoing()
                elif neuron.id is 3:                                                #   Food angle
                    ang = self.closest_food_angle
                    neuron.val = ang / 180 if ang <= 180 else (ang - 360) / 180
                    neuron.pass_to_outgoing()
                elif neuron.id is 4:                                                #   Creature dist
                    neuron.val = self.closest_creature_dist / 1416
                    neuron.pass_to_outgoing()
                elif neuron.id is 5:                                                #   Creature angle
                    ang = self.closest_creature_angle
                    neuron.val = ang / 180 if ang <= 180 else (ang - 360) / 180
                    neuron.pass_to_outgoing()
                elif neuron.id is 6:                                                #   Wall dist
                    neuron.val = self.closest_wall_dist / 375
                    neuron.pass_to_outgoing()
                elif neuron.id is 7:                                                #   Wall angle
                    ang = self.closest_wall_angle
                    neuron.val = ang / 180 if ang <= 180 else (ang - 360) / 180
                    neuron.pass_to_outgoing()
                elif neuron.id is 8:                                                #   Bias
                    neuron.val = 1
                    neuron.pass_to_outgoing()
                else:
                    neuron.val = 0

    def reset_brain(self):
        for neuron in self.neurons.values():
            neuron.val = 0

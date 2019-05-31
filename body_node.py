import random


class BodyNode:

    def __init__(self, body_part_type, strength, angle, size, pos, constraint):
        r = random.randint(0, 100)
        r2 = random.randint(0, 100)
        r3 = random.randint(0, 100)
        r4 = random.randint(0, 100)
        self.part_type = body_part_type

        if body_part_type is not "body":
            if r < 80:
                self.strength = strength
            elif r < 90:
                self.strength = max(0, min(100, strength + (90 - r) - (5 if r < 85 else 4)))
            else:
                self.strength = random.randint(0, 100)

            if r2 < 80:
                self.angle = angle
            elif r2 < 90:
                self.angle = angle + (90 - r2) - (5 if r2 < 85 else 4) % 360
            else:
                self.angle = random.randint(0, 359)

            if r3 < 80:
                self.position = (max(3 if self.part_type is "eye" else int(constraint / 8),
                                     min(constraint, pos)))
            elif r3 < 90:
                self.position = max(3 if self.part_type is "eye" else int(constraint / 8),
                                    min(constraint, pos + (90 - r3) - (5 if r3 < 85 else 4)))
            else:
                self.position = random.randint(3 if self.part_type is "eye" else int(constraint / 8),
                                               constraint)

            if r4 < 80:
                self.size = max(3 if self.part_type is "spike" else 0,
                                min(constraint, pos))
            elif r4 < 90:
                self.size = max(3 if self.part_type is "spike" else 0,
                                min(constraint, pos + (90 - r4) - (5 if r4 < 85 else 4)))
            else:
                self.size = random.randint(3 if self.part_type is "spike" else 0,
                                           constraint)

        else:
            if r < 80:
                self.strength = strength
            elif r < 90:
                self.strength = max(1, min(201, strength + (90 - r) - (5 if r < 85 else 4)))
            else:
                self.strength = random.randint(1, 201)

            if r2 < 80:
                self.angle = angle
            elif r2 < 90:
                self.angle = max(1, min(201, angle + (90 - r2) - (5 if r2 < 85 else 4)))
            else:
                self.angle = random.randint(1, 201)

            if r3 < 80:
                self.position = pos
            elif r3 < 90:
                self.position = max(1, min(201, pos + (90 - r3) - (5 if r3 < 85 else 4)))
            else:
                self.position = random.randint(1, 201)

            if r4 < 80:
                self.size = size
            elif r4 < 90:
                self.size = max(5, min(25, size + (90 - r4) - (5 if r4 < 85 else 4)))
            else:
                self.size = random.randint(5, 25)

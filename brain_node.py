import random


class BrainNode:

    def __init__(self, node_type, children, id):
        self.id = id
        self.val = 0
        self.node_type = node_type
        self.outgoing = children

    def pass_to_outgoing(self):
        for connection in self.outgoing.values():
            connection[1].val = connection[1].val + (self.val * connection[0])
            connection[1].pass_to_outgoing()

    def mutate(self):
        r = random.randint(1, 100)
        if r < 10 and len(self.outgoing.values()) > 0:
            r2 = random.randint(0, len(self.outgoing.values()) - 1)
            cweight = self.outgoing[r2][0]
            if r < 5:
                if len(self.outgoing.values()) > 0:
                    self.outgoing[r2][0] = random.randint(0, 200) / 100 - 1
            else:
                self.outgoing[r2][0] = max(-1, min(1, cweight + random.randint(0, 20) / 100 - 0.1))
        return self

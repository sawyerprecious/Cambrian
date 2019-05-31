import random
import body_node
import brain_node


class Genome:

    def __init__(self, genes, copy=False):
        self.fitness = 0
        self.brain_nodes = {}
        if genes is None:
            self.body_nodes = {0: body_node.BodyNode("body",
                                                     random.randint(1, 201),
                                                     random.randint(1, 201),
                                                     random.randint(5, 25),
                                                     random.randint(1, 201),
                                                     0)}
            self.brain_nodes = self.create_brain()

        elif copy:
            self.body_nodes = genes.body_nodes
            self.brain_nodes = genes.brain_nodes

        else:
            for i in range(0, len(genes.brain_nodes.values())):
                self.brain_nodes[i] = genes.brain_nodes[i].mutate()

            new_nodes = {}
            angles = {0, 180}
            for i in (range(len(genes.body_nodes))):
                node = genes.body_nodes.get(i)
                if not isinstance(node, type(None)):
                    angles.add(node.angle)
                    flag = False
                    for k in range(5):
                        created_node = (body_node.BodyNode(node.part_type,
                                                           node.strength,
                                                           node.angle,
                                                           node.size,
                                                           node.position,
                                                           0 if i is 0 else new_nodes.get(0).size))
                        if self.check_angles(created_node.angle, angles):
                            flag = True
                            break
                    if created_node.strength > 0 and flag:
                        new_nodes[len(new_nodes)] = created_node
            self.body_nodes = new_nodes
            node_0 = new_nodes.get(0)
            r = random.randint(0, 100)
            if r < 3:
                new_mutation = (body_node.BodyNode("eye",
                                                   random.randint(1, 15),
                                                   random.randint(0, 359),
                                                   0,
                                                   random.randint(1, int(node_0.size)),
                                                   int(node_0.size)))
                if self.check_angles(new_mutation.angle, angles):
                    new_nodes[len(genes.body_nodes)] = new_mutation

                new_mutation2 = body_node.BodyNode(new_mutation.part_type,
                                                   new_mutation.strength,
                                                   360 - new_mutation.angle,
                                                   new_mutation.size,
                                                   new_mutation.position,
                                                   node_0.size)
                if self.check_angles(new_mutation2.angle, angles):
                    new_nodes[len(genes.body_nodes) + 1] = new_mutation2

            elif r < 6:
                new_mutation = (body_node.BodyNode("spike",
                                                   random.randint(5, 15),
                                                   random.randint(0, 359),
                                                   random.randint(int(node_0.size / 4),
                                                                  node_0.size),
                                                   random.randint(int(node_0.size * 1.2),
                                                                  node_0.size * 2),
                                                   node_0.size * 2))
                if self.check_angles(new_mutation.angle, angles):
                    new_nodes[len(genes.body_nodes)] = new_mutation

                new_mutation2 = body_node.BodyNode(new_mutation.part_type,
                                                   new_mutation.strength,
                                                   360 - new_mutation.angle,
                                                   new_mutation.size,
                                                   new_mutation.position,
                                                   node_0.size * 2)
                if self.check_angles(new_mutation2.angle, angles):
                    new_nodes[len(genes.body_nodes) + 1] = new_mutation2

            elif r < 9:
                new_mutation = (body_node.BodyNode("flagella",
                                                   random.randint(5, 15),
                                                   random.randint(0, 359),
                                                   0,
                                                   random.randint(int(node_0.size * 1.2),
                                                                  node_0.size * 2),
                                                   node_0.size * 2))
                if self.check_angles(new_mutation.angle, angles):
                    new_nodes[len(genes.body_nodes)] = new_mutation

                new_mutation2 = body_node.BodyNode(new_mutation.part_type,
                                                                      new_mutation.strength,
                                                                      360 - new_mutation.angle,
                                                                      new_mutation.size,
                                                                      new_mutation.position,
                                                                      node_0.size * 2)

                if self.check_angles(new_mutation2.angle, angles):
                    new_nodes[len(genes.body_nodes) + 1] = new_mutation2

            while len(self.body_nodes) > 7:
                self.body_nodes.pop(len(self.body_nodes) - 1)

    def check_angles(self, angle, existing_list):
        flag = True
        for ang in existing_list:
            if 360 + (ang - 10) % 360 <= angle <= (ang + 10) % 360:
                flag = False
        return flag

    def create_brain(self):
        outputs = []
        mid = []
        # output:
        for i in range(0, 3):
            new_node = brain_node.BrainNode("output", {}, 15 + i)
            outputs.append(new_node)
            self.brain_nodes[15 + i] = new_node
        # middle layer:
        for i in range(0, 6):
            new_node = brain_node.BrainNode("middle", self.set_children(outputs), 9 + i)
            mid.append(new_node)
            self.brain_nodes[9 + i] = new_node
        # input:
        for i in range(0, 9):
            new_node = brain_node.BrainNode("input", self.set_children(mid), i)
            self.brain_nodes[i] = new_node
        return self.brain_nodes

    def set_children(self, children):
        to_return = {}
        i = 0
        for child in children:
            to_return[i] = [random.randint(0, 200) / 100 - 1, child]
            i += 1
        return to_return

    def genetic_distance(self, other_genome):
        difference_num_eyes = 0
        difference_num_spikes = 0
        difference_num_flag = 0
        difference_body = 0
        for node in self.body_nodes.values():
            if node.part_type is "eye":
                difference_num_eyes += 1
            elif node.part_type is "spike":
                difference_num_spikes += 1
            elif node.part_type is "flagella":
                difference_num_flag += 1
            elif node.part_type is "body":
                difference_body += node.size / 5

        for node in other_genome.body_nodes.values():
            if node.part_type is "eye":
                difference_num_eyes -= 1
            elif node.part_type is "spike":
                difference_num_spikes -= 1
            elif node.part_type is "flagella":
                difference_num_flag -= 1
            elif node.part_type is "body":
                difference_body -= node.size / 5

        difference_num_flag = abs(difference_num_flag)
        difference_num_spikes = abs(difference_num_spikes)
        difference_num_eyes = abs(difference_num_eyes)
        difference_body = abs(difference_body)

        body_dist = difference_num_flag + difference_num_spikes + difference_num_eyes + difference_body

        difference_weight = 0

        for i in range(len(self.brain_nodes)):
            for j in range(len(self.brain_nodes[i].outgoing)):
                difference_weight += abs(self.brain_nodes[i].outgoing[j][0]
                                         - other_genome.brain_nodes[i].outgoing[j][0])

        return body_dist + difference_weight / 10

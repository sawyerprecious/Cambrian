import random
import body_node


class Genome:

    def __init__(self, genes, copy=False):
        self.fitness = 0
        # TODO: setup brain genes
        if genes is None:
            self.body_nodes = {0: body_node.BodyNode("body",
                                                     random.randint(1, 201),
                                                     random.randint(1, 201),
                                                     random.randint(5, 25),
                                                     random.randint(1, 201),
                                                     0)}

        elif copy:
            self.body_nodes = genes.body_nodes

        else:
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

        self.brain_nodes = {}
        self.brain_connections = {}

    def check_angles(self, angle, existing_list):
        flag = True
        for ang in existing_list:
            if 360 + (ang - 10) % 360 <= angle <= (ang + 10) % 360:
                flag = False
        return flag

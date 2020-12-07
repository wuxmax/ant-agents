from node import Node
from edge import Edge
import random


class Graph(object):

    def __init__(self, params):
        self.x_size = params['size_x']
        self.y_size = params['size_y']
        self.nodes = self.create_nodes()
        if params['thickness']:
            self.edges = self.create_labyrinth_edges(self.x_size, self.y_size)
        else:
            self.edges = self.create_edges(self.x_size, self.y_size)
        if params['f'] == 0 and params['e'] == 0:
            if params['a'] == 0:
                self.nest = self.choose_nest()
                self.add_food(params['food_src_count'], params['food_max'], params['food_min'])
            else:
                self.nodes[(4, 3)].nest = True
                self.nest = self.nodes[(4, 3)]
                self.nodes[(6, 7)].add_food(500)
                self.nodes[(6, 2)].add_food(500)
                self.nodes[(1, 1)].add_food(500)
                self.nodes[(2, 5)].add_food(500)
        if params['e'] and not params['f']:
            self.create_suboptimal_path()
        if params['f'] and not params['e']:
            self.create_interrupted_path()

    # verringert auf allen kanten die pheromonstärke nach den parametern
    def evaporate(self, evaporation, evap_type):
        for edge in self.edges:
            edge.evaporate(evaporation, evap_type)

    def add_food(self, number, maxamount, minamount):
        xylist = []
        for x in range(1, (self.x_size + 1)):
            for y in range(1, (self.y_size + 1)):
                if x != self.nest.get_x() and y != self.nest.get_y():
                    xylist.append((x, y))
        random.shuffle(xylist)
        sources = xylist[:number]
        for (x, y) in sources:
            self.nodes.get((x, y)).add_food(random.randint(minamount, maxamount))

    def create_edges(self, max_x, max_y):
        edges = []
        for (x, y) in self.nodes:
            me = self.nodes.get((x, y))
            if x < max_x:
                right = self.nodes.get(((x + 1), y))
                edges.append(Edge(me, right))
            if y < max_y:
                down = self.nodes.get((x, (y + 1)))
                edges.append(Edge(me, down))
        return edges

    def neighbours_node(self, node):
        x = node.get_x()
        y = node.get_y()
        neighbours = []
        neighbours.append(self.nodes.get((x - 1, y)))
        neighbours.append(self.nodes.get((x + 1, y)))
        neighbours.append(self.nodes.get((x, y - 1)))
        neighbours.append(self.nodes.get((x, y + 1)))
        return [i for i in neighbours if i is not None]

    def create_labyrinth_edges(self, x, y):
        edges = []
        nodes = list(self.nodes.values())
        current_nodes = []
        current_nodes.append(self.nodes.get((int(x/2), int(y/2))))
        nodes = list(filter(lambda v: v not in current_nodes, nodes))
        while nodes:
            new_current = []
            for node in current_nodes:
                new_current.append(node)
                neighbours = self.neighbours_node(node)
                random.shuffle(neighbours)
                for neighbour in neighbours:
                    if neighbour in nodes:
                        if random.randint(0, 100) > 50:
                            edges.append(Edge(node, neighbour))
                            new_current.append(neighbour)
                            nodes.remove(neighbour)
            current_nodes = new_current
        return edges

    def choose_nest(self):
        a = random.randint(1, self.x_size)
        b = random.randint(1, self.y_size)
        self.nodes[(a, b)].nest = True
        self.nodes[(a, b)].value = 0
        return self.nodes[(a, b)]

    def create_nodes(self):
        nodes = {}
        for x in range(1, self.x_size + 1):
            for y in range(1, self.y_size + 1):
                add_me = Node(0, [], x, y)
                nodes[(x, y)] = add_me
        return nodes

    def create_suboptimal_path(self):
        self.nest = self.nodes[(1, 1)]
        self.nodes[(1,1)].nest = 1
        self.nodes[(4, 3)].add_food(1000)
        for edge in self.edges:
            if edge.has_nodes(self.nodes[(1,1)], self.nodes[(2,1)]):
                edge.food_pheromone = 1
            if edge.has_nodes(self.nodes[(2,1)], self.nodes[(2,2)]):
                edge.food_pheromone = 1
            if edge.has_nodes(self.nodes[(2,2)], self.nodes[(2,3)]):
                edge.food_pheromone = 1
            if edge.has_nodes(self.nodes[(2,3)], self.nodes[(2,4)]):
                edge.food_pheromone = 1
            if edge.has_nodes(self.nodes[(2,4)], self.nodes[(3, 4)]):
                edge.food_pheromone = 1
            if edge.has_nodes(self.nodes[(3,4)], self.nodes[(4,4)]):
                edge.food_pheromone = 1
            if edge.has_nodes(self.nodes[(4,4)], self.nodes[(4,3)]):
                edge.food_pheromone = 1

    def create_interrupted_path(self):
        self.nest = self.nodes[(1, 1)]
        self.nodes[(1,1)].nest = 1
        self.nodes[(4, 4)].add_food(500)
        for edge in self.edges:
            if edge.has_nodes(self.nodes[(1,1)], self.nodes[(2,1)]):
                edge.food_pheromone = 2
            if edge.has_nodes(self.nodes[(2,1)], self.nodes[(2,2)]):
                edge.food_pheromone = 2
            if edge.has_nodes(self.nodes[(2,2)], self.nodes[(2,3)]):
                edge.node1.edges.remove(edge)
                edge.node2.edges.remove(edge)
                self.edges.remove(edge)
            if edge.has_nodes(self.nodes[(2,3)], self.nodes[(2,4)]):
                edge.food_pheromone = 2
            if edge.has_nodes(self.nodes[(2,4)], self.nodes[(3, 4)]):
                edge.food_pheromone = 2
            if edge.has_nodes(self.nodes[(3,4)], self.nodes[(4,4)]):
                edge.food_pheromone = 2

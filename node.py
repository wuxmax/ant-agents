from math import inf
import random

class Node(object):
    def __init__(self, food, edges, x_pos, y_pos):  # initializes a single node and associates a list of edges to it
        self.food = food  # int, x if nest, 0 else
        self.edges = edges  # list of edges, can be empty, argument has to be 'None' for this to happen
        self.x_pos = x_pos  # x position
        self.y_pos = y_pos  # y position
        self.nest = False  # Muss das wissen damit die Ameisen das ohne auf den graphen zuzugreifen wissen können
        self.value = inf

    def add_food(self, amount):
        self.food = amount

    def add_pheromone(self, coming_from, food, nest):
        for edge in self.edges:
            if edge.has_node(coming_from):
                edge.add_pheromone(food, nest)

    def set_pheromone(self, coming_from, food, nest):
        for edge in self.edges:
            if edge.has_node(coming_from):
                edge.set_pheromone(food, nest)

    def set_pheromone_2(self, coming_from, food):
        for edge in self.edges:
            if edge.has_node(coming_from):
                edge.set_pheromone_2(food)
                return

    def equal(self, node):
        return self.get_x() == node.get_x() and self.get_y() == node.get_y()

    def not_equal(self, node):
        return self.get_x() != node.get_x() or self.get_y() != node.get_y()

    def set_nestdist(self, value):
        self.value = value

    def has_food(self):
        return self.food > 0

    def get_x(self):  # funktion zum abfragen der x position
        return self.x_pos

    def get_y(self):  # funktion zum abfragen der y position
        return self.y_pos

    def get_x_y(self):  # funktion zum abfragen der x und y positionen
        return (self.x_pos, self.y_pos)

    def neighbours(self):
        nodes = list(map(lambda x: x.other_node(self), self.edges))
        return list(filter(lambda x: not (x.value == -1), nodes))

    def neighbours_visited(self):
        return list(filter(lambda x: not (x.value == inf), self.neighbours()))

    def neighbours_not_visited(self):
        return list(filter(lambda x: x.value == inf, self.neighbours()))

    def highest_neighbour(self):
        nodes = self.neighbours_visited()
        # dieser Fall tritt nur beim Start auf.
        if len(nodes) == 0:
            return random.choice(self.neighbours_not_visited())
        nodes = list(sorted(nodes, key=lambda x: x.value, reverse=True))
        # print(list(map(lambda x: x.value, nodes)))
        nodes = list(filter(lambda x: x.value == nodes[0].value, nodes))
        # print(list(map(lambda x: x.value, nodes)))
        return random.choice(nodes)

    def smallest_neighbours(self):
        if self.neighbours_visited():
            nodes = sorted(self.neighbours_visited(), key=lambda x: x.value, reverse=False)
            nodes = list(filter(lambda x: x.value == nodes[0].value, nodes))
            return nodes
        return False

    def smallest_nestdist_to_field(self):
        if not self.smallest_neighbours():
            return self.value
        return min(self.smallest_neighbours()[0].value + 1, self.value)

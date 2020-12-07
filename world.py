from graph import Graph
from ants import Ants
from ants import Explorer
from ants import Carrier
from random import randint

class World(object):
    graph = None
    ants = None
    explorer = None
    carrier = None

    def __init__(self, params):
        self.ant_greediness = params['greediness']
        self.ant_greediness_food = params['greediness_food']
        self.ants_init = params['ants_init']
        self.ants_max = params['ants_max']
        self.carriers_init = params['carriers_init']
        self.explorer_init = params['explorers_init']
        self.explorers_max = params['explorers_max']
        self.carriers_max = params['carriers_max']
        self.probability_new_ant = params['probability_new_ant']
        self.probability_new_explorer = params['probability_new_explorer']
        self.probability_new_carrier = params['probability_new_carrier']
        self.evaporation = params['evaporation']
        self.evaporation_type = params['evaporation_type']
        self.wait = params['wait']
        self.graph = Graph(params)
        self.ants = []
        self.explorers = []
        self.carriers = []

    def populate(self):
        for i in range(self.ants_init):
            ant = Ants(self.graph.nest, self.graph.nest, self.graph.nest, False, 0, self.ant_greediness, self.ant_greediness_food)
            ant.attr = i
            self.ants.append(ant)

    def populate_explorers(self):
        for i in range(self.explorer_init):
            explorer = Explorer(self.graph.nest, self.graph.nest, self.graph.nest, False)
            explorer.attr = i
            self.explorers.append(explorer)

    def populate_carriers(self):
        for i in range(self.carriers_init):
            carrier = Carrier(self.graph.nest, self.graph.nest, self.graph.nest, False, False)
            carrier.attr = i
            self.carriers.append(carrier)

    def create_ant(self):
        if len(self.ants) >= self.ants_max:
            return
        if randint(0, 100) < self.probability_new_ant:
            ant = Ants(self.graph.nest, self.graph.nest, self.graph.nest, 0, 0, self.ant_greediness,
                       self.ant_greediness_food)
            self.ants.append(ant)

    def create_explorer(self):
        if len(self.explorers) >= self.explorers_max:
            return
        if randint(0, 100) < self.probability_new_explorer:
            explorer = Explorer(self.graph.nest, self.graph.nest, self.graph.nest, False, False)
            self.explorers.append(explorer)

    def create_carrier(self):
        if len(self.carriers) >= self.carriers_max:
            return
        if randint(0, 100) < self.probability_new_carrier:
            carrier = Carrier(self.graph.nest, self.graph.nest, self.graph.nest, False, False)
            self.carriers.append(carrier)

    def simulate_cycle(self):
        if self.wait == 1:
            input("Press Enter to continue...")
        for ant in self.ants:
            ant.action()
        for ant in self.ants:
            ant.add_pheromone()
        self.create_ant()
        self.graph.evaporate(self.evaporation, self.evaporation_type)

    def simulate_cycle_explorer_carrier(self):
        if self.wait == 1:
            input("Press Enter to continue...")
        for explorer in self.explorers:
            explorer.action()
        for explorer in self.explorers:
            explorer.set_nodes()
        for explorer in self.explorers:
            explorer.action()
        for explorer in self.explorers:
            explorer.set_nodes()

        for carrier in self.carriers:
            carrier.action()
        for carrier in self.carriers:
            if carrier.pheromone_modification:
                carrier.modify_pheromone()

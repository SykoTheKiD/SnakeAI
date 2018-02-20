import logging
import random

from ann import NeuralNetwork

POPULATION_SIZE = 5
NUM_GENERATIONS = 1000000

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def crossover(mother, father):
    mother_size = len(mother.network.layers)
    rand_point = random.randint(0, mother_size - 1)
    i = rand_point
    child = mother
    while i < mother_size:
        mother_bias = mother.network.layers[i]['biases']
        father.network.layers[i]['biases'] = mother_bias
        i += 1
        child = mother if random.randint(0, 1) else father
    return child


class GeneticAlgorithm:
    def __init__(self, max_size, top_k):
        self.population_max_size = max_size
        self.top_agents_size = top_k
        if self.population_max_size < self.top_agents_size:
            self.top_agents_size = self.population_max_size
        self.population = []
        self.iteration = 1
        self.mutation_rate = 1
        self.best_agent = None

    def reset(self):
        self.iteration = 1
        self.mutation_rate = 1
        self.best_agent = None

    def generate_population(self):
        self.population = []
        for i in range(self.population_max_size):
            agent = Agent(i, NeuralNetwork())
            self.population.append(agent)
        print(self.population)

    @staticmethod
    def predict(agent, input_vector):
        return agent.network.predict(input_vector)

    def evolve(self):
        top_class = self.select()
        if self.mutation_rate == 1 and top_class[0].fitness < 0:
            self.generate_population()
        else:
            self.mutation_rate = 0.2

        i = self.top_agents_size
        while i < self.population_max_size:
            if i == self.top_agents_size:
                mother = top_class[0]
                father = top_class[1]
                child = crossover(mother, father)
            elif i < self.population_max_size - 2:
                mother = random.choice(top_class)
                father = random.choice(top_class)
                child = crossover(mother, father)
            else:
                child = random.choice(top_class)

            child.id = self.population[i].id
            child.fitness = 0
            child.high_score = 0
            child.top_class = False
            self.population[i] = child
            i += 1

        if top_class[0].fitness > self.best_agent.fitness:
            self.best_agent = top_class[0]

    def select(self):
        self.population.sort(key=lambda agent: agent.fitness, reverse=True)
        for i in range(self.top_agents_size):
            self.population[i].top_class = True
        return self.population[:self.top_agents_size]

    def mutation(self, child):
        for i in range(len(child.network.layers)):
            child.network.layers[i]['biases'] = self.mutate(child.network.layers[i]['biases'])

        for i in range(len(child.network.layers)):
            child.network.layers[i]['weights'] = self.mutate(child.network.layers[i]['weight'])

        return child

    def mutate(self, offspring):
        if random.random() < self.mutation_rate:
            factor = 1 + ((random.random() - 0.5) * 3 + (random.random() - 0.5))
            offspring *= factor
        return offspring


class Agent:
    def __init__(self, agent_id, network):
        self.id = agent_id
        self.high_score = 0
        self.fitness = -1
        self.network = network
        self.top_class = False

    def __str__(self):
        return str(self.id)

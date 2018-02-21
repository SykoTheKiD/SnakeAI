import random

import tensorflow as tf

from ann import NeuralNetwork


class GenAlgo:
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = []
        self.init_population()

    def init_population(self):
        for _ in range(self.population_size):
            self.population.append(Agent())

    def select(self):
        self.population = sorted(self.population, key=lambda snake: snake.fitness, reverse=True)
        self.population = self.population[:int(0.2 * len(self.population))]

    def crossover(self):
        children = []
        for _ in range((self.population_size - len(self.population)) // 2):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            pop_slice = random.randrange(0, len(parent1.network.layers))
            parent1 = parent1.network.layers[:pop_slice]
            parent2 = parent2.network.layers[:pop_slice]
            child1 = Agent()
            child1.network.layers = parent1 + parent2[pop_slice:]
            child2 = Agent()
            child2.network.layers = parent2 + parent1[pop_slice:]
            children.append(child1)
            children.append(child2)

        self.population.extend(children)

    def mutate(self):
        for snake in self.population:
            if random.uniform(0.0, 1.0) <= 0.1:
                layer1 = random.choice(snake.network.layers)
                layer2 = random.choice(snake.network.layers)
                while layer2 == layer1:
                    layer2 = random.choice(snake.network.layers)
                mult_vector1_weights = tf.random_normal(shape=layer1['weights'].shape)
                mult_vector1_biases = tf.random_normal(shape=layer1['biases'].shape)
                mult_vector2_weights = tf.random_normal(shape=layer2['weights'].shape)
                mult_vector2_biases = tf.random_normal(shape=layer2['biases'].shape)
                with tf.Session() as sess:
                    sess.run(tf.global_variables_initializer())
                    result = sess.run(
                        [tf.multiply(layer1['weights'], mult_vector1_weights),
                         tf.multiply(layer1['biases'], mult_vector1_biases),
                         tf.multiply(layer2['weights'], mult_vector2_weights),
                         tf.multiply(layer2['biases'], mult_vector2_biases)
                         ]
                    )
                    layer1['weights'] = result[0]
                    layer1['biases'] = result[1]
                    layer2['weights'] = result[2]
                    layer2['biases'] = result[3]


class Agent:
    def __init__(self):
        self.network = NeuralNetwork()
        self.fitness = -1

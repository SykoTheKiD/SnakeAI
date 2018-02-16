POPULATION_SIZE = 5
NUM_GENERATIONS = 1000000

class Agent:
	def __init__(self, high_score):
		self.high_score = 0
		self.fitness = -1


def genetic_algorithm():
	agents = init_agents(POPULATION_SIZE)

	for generation in tqdm(range(NUM_GENERATIONS)):
		agents = fitness(agents)
		agents = selection(agents)
		agents = crossover(agents)
		agents = mutation(agents)

		if any(agent.fitness >=90 for agent in agents):
			logger.info("Complete")
			exit(0)

def init_agents(population_size):
	pass

def fitness(agents):
	pass

def selection(agents):
	pass

def crossover(agents):
	pass

def mutation(agents):
	pass
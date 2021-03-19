import numpy as np
import math
import random
from Rocket import Rocket

class Evolutionizer():

    def __init__(self, START_X, START_Y, ROCKET_SIZE, MUTATION_THRESHOLD, MUTATION_SCALE_FACTOR, ITERATIONS, NUMBER_OF_ROCKETS, MOVE, SIMULATION_WIDTH, SIMULATION_HEIGHT):
        self.START_X = START_X
        self.START_Y = START_Y
        self.ROCKET_SIZE = ROCKET_SIZE
        self.MUTATION_THRESHOLD = MUTATION_THRESHOLD
        self.MUTATION_SCALE_FACTOR = MUTATION_SCALE_FACTOR
        self.NUMBER_OF_ROCKETS = NUMBER_OF_ROCKETS
        self.ITERATIONS = ITERATIONS
        self.MOVE = MOVE
        self.SIMULATION_WIDTH = SIMULATION_WIDTH
        self.SIMULATION_HEIGHT = SIMULATION_HEIGHT

    def mutate(self, rocket):
        new_genes = []
        for gene in rocket.genes:
            rng = random.randrange(0,100)/100
            direction = random.randint(0,2)
            if rng < self.MUTATION_THRESHOLD:
                direction = random.randint(0,2)
                if direction < 1:
                    new_genes.append(gene+(gene*self.MUTATION_SCALE_FACTOR))
                else:
                    new_genes.append(gene-(gene*self.MUTATION_SCALE_FACTOR))
            else:
                new_genes.append(gene)
        rocket.genes = np.array(new_genes)
        return rocket

    def crossover(self, rocket_1, rocket_2, mode="Chunk"):
        if mode == "Chunk":
            chunk_index = random.randint(0,self.ITERATIONS)
            rocket_1_genes = rocket_1.genes[:chunk_index]
            rocket_2_genes = rocket_2.genes[chunk_index:]
            new_rocket = Rocket(self.START_X, self.START_Y, self.ROCKET_SIZE, self.ITERATIONS, self.MOVE, self.SIMULATION_WIDTH, self.SIMULATION_HEIGHT)
            new_rocket.genes = np.vstack([rocket_1_genes, rocket_2_genes])
        else:
            pass
        return new_rocket

    def calc_fitness(self, rocket, goal):
        if rocket.collided:
            fitness = math.sqrt((rocket.loc[0]-goal.loc[0])**2 + (rocket.loc[1]-goal.loc[1])**2)
            return 0

        if rocket.finished:
            fitness = 20
            return 1

        distance = math.sqrt((rocket.loc[0]-goal.loc[0])**2 + (rocket.loc[1]-goal.loc[1])**2)
        fitness = 1/distance

        if fitness > rocket.fitness:
            rocket.fitness = fitness
            return fitness
        else:
            return rocket.fitness

    def create_next_population(self, population):
        next_population = []
        mating_pool = []

        # Populate mating pool
        for rocket in population:
            for _ in range(0, int(rocket.fitness*500)+1):
                mating_pool.append(rocket)

        # Pick parents at random
        for number in range(self.NUMBER_OF_ROCKETS):
            r_1 = random.choice(mating_pool)
            r_2 = random.choice(mating_pool)
            new_rocket = self.crossover(r_1, r_2)
            new_rocket_mutated = self.mutate(new_rocket)
            next_population.append(new_rocket_mutated)

        return next_population

    def calc_population_fitness(self, population, goal, mean=True):
        fitness_sum = 0
        for rocket in population:
            fitness_sum += self.calc_fitness(rocket, goal)

        if mean:
            return fitness_sum/len(population)
        else:
            return fitness_sum

    def create_initial_population(self):
        population = []
        for rocket_number in range(self.NUMBER_OF_ROCKETS):
            population.append(Rocket(self.START_X, self.START_Y, self.ROCKET_SIZE, self.ITERATIONS, self.MOVE, self.SIMULATION_WIDTH, self.SIMULATION_HEIGHT))
        return population

    def print_population_info(self, population, goal):
        print(f"Population size: {len(population)}")
        print(f"Population fitness: {self.calc_population_fitness(population, goal, False)}")
        print(f"Population fitness (mean): {self.calc_population_fitness(population, goal, True)}")

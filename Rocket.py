import numpy as np
import math
import random

class Rocket:

    def __init__(self, START_X, START_Y, ROCKET_SIZE, ITERATIONS, MOVE, SIMULATION_WIDTH, SIMULATION_HEIGHT):
        self.loc = np.array([START_X, START_Y])
        self.dir = np.array([0,0])
        self.acc = np.array([0,0])
        self.fitness = 0.00001
        self.collided = False
        self.finished = False
        self.size = ROCKET_SIZE
        self.ITERATIONS = ITERATIONS
        self.MOVE = MOVE
        self.SIMULATION_WIDTH = SIMULATION_WIDTH
        self.SIMULATION_HEIGHT = SIMULATION_HEIGHT
        self.genes = self.create_genes()

    def create_genes(self):
        genes = []
        for i in range(self.ITERATIONS):
            genes.append([float(random.randrange(int(-self.MOVE),int(self.MOVE)*2)), float(random.randrange(int(-self.MOVE),int(self.MOVE)*2))])
        return np.array(genes)

    def __str__(self):
        print("### ROCKET ###")
        print(f"Location: {self.loc}")
        print(f"Direction: {self.dir}")
        print(f"Acceleration: {self.acc}")
        print(f"Genes: {self.genes}")
        print(f"Fitness: {self.fitness}")
        return ""

    def update(self, iteration, goal, obstacle):
        self.loc = self.loc + self.dir
        self.dir = self.dir + self.acc
        self.acc = self.acc + self.genes[iteration]

        # Check collision with borders
        if not self.size < self.loc[0] < self.SIMULATION_WIDTH-self.size:
            self.dir = np.array([0,0])
            self.collided = True

        if not self.size <= self.loc[1] < self.SIMULATION_HEIGHT-self.size:
            self.dir = np.array([0,0])
            self.collided = True

        # Check collision with obstacles
        if math.sqrt((self.loc[0]-goal.loc[0])**2 + (self.loc[1]-goal.loc[1])**2) < 22:
            self.dir = np.array([0,0])
            self.finished = True

        # Check collision with goal

import numpy as np
import math

class Goal:

    def __init__(self, SIMULATION_WIDTH, SIMULATION_HEIGHT, GOAL_SIZE):
        self.loc = np.array([int(SIMULATION_WIDTH/2),int(SIMULATION_HEIGHT-(SIMULATION_HEIGHT*0.9))])
        self.radius = GOAL_SIZE

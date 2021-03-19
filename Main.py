import cv2
import numpy as np
from Obstacles import RectangularObstacle
from Goals import Goal
from Rocket import Rocket
from Evolutionizer import Evolutionizer


# Define Hyperparameters

# Goal
SIMULATION_WIDTH = 12800
SIMULATION_HEIGHT = 9000
GOAL_SIZE = 60

# Rockets
START_X = SIMULATION_WIDTH/2
START_Y = SIMULATION_HEIGHT-(SIMULATION_HEIGHT*0.1)
NUMBER_OF_ROCKETS = 200
ROCKET_SIZE = 30

# Screen
SCREEN_WIDTH = SIMULATION_WIDTH/10
SCREEN_HEIGHT = SIMULATION_HEIGHT/10

# Evolution
ITERATIONS = 100
MUTATION_THRESHOLD = 0.1
MUTATION_SCALE_FACTOR = 0.2
MOVE = SIMULATION_WIDTH/10000
FPS = 40
STEPS = 50

# Drawing method
def show_canvas(canvas):
    canvas_resized = cv2.resize(canvas, (int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))
    cv2.imshow("Smart Rockets", canvas_resized)
    cv2.waitKey(int(1000/FPS))

# Init Stuff
evol = Evolutionizer(START_X, START_Y, ROCKET_SIZE, MUTATION_THRESHOLD, MUTATION_SCALE_FACTOR, ITERATIONS, NUMBER_OF_ROCKETS, MOVE, SIMULATION_WIDTH, SIMULATION_HEIGHT)
goal = Goal(SIMULATION_WIDTH, SIMULATION_HEIGHT, GOAL_SIZE)
obstacle = RectangularObstacle(250, 250,300, 50)
population = evol.create_initial_population()

# Go!
for step in range(STEPS):
    print(f"Step: {step}")
    for iteration in range(ITERATIONS):

        # Create empty canvas
        canvas = np.zeros((SIMULATION_HEIGHT,SIMULATION_WIDTH), np.uint8)

        # Draw Goal
        canvas = cv2.circle(canvas, (goal.loc[0]-10, goal.loc[1]), goal.radius, (255,255,255), cv2.FILLED)

        # Draw Obstacles
        #canvas = cv2.rectangle(canvas, (obstacle.x1, obstacle.y1), (obstacle.x2, obstacle.y2), (255,255,255), cv2.FILLED)

        # Draw each Rocket
        for rocket in population:
            canvas = cv2.circle(canvas, (int(rocket.loc[0]-1), int(rocket.loc[1]-1)), rocket.size, (200,255,200), cv2.FILLED)

        # Plot canvas
        show_canvas(canvas)

        # Simulate step
        for rocket in population:
            rocket.update(iteration, goal, obstacle)

    # Calculate fitness
    for rocket in population:
        evol.calc_fitness(rocket, goal)

    # Show population infos
    evol.print_population_info(population, goal)

    # Create next population
    population = evol.create_next_population(population)

cv2.destroyAllWindows()

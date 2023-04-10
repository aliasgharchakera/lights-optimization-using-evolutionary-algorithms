import numpy as np
import random
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Define the problem
ROOM_WIDTH = 10
ROOM_HEIGHT = 10
NUM_LIGHTS = 5

# Define the fitness function
def evaluate_fitness(individual):
    # Create an array to represent the room with the lights
    room = np.zeros((ROOM_WIDTH, ROOM_HEIGHT))
    for light in individual:
        x, y, intensity = light[0], light[1], light[2]
        # Add the light to the room
        room[x][y] += intensity
    # Calculate the energy consumption and brightness level
    energy_consumption = np.sum(room)
    brightness_level = np.average(room)
    # Return the fitness as a tuple
    return energy_consumption, -brightness_level

# Define the genetic operators
def generate_light():
    # Generate a random light with position and intensity
    x = random.randint(0, ROOM_WIDTH - 1)
    y = random.randint(0, ROOM_HEIGHT - 1)
    intensity = random.uniform(0, 1)
    light = (x, y, intensity)
    print(light)  # <-- Add this line to check the generated light
    return light


def mutate_light(light, indpb):
    # Mutate the position and/or intensity of the light with probability indpb
    x, y, intensity = light[0], light[1], light[2]
    if random.random() < indpb:
        x = random.randint(0, ROOM_WIDTH - 1)
    if random.random() < indpb:
        y = random.randint(0, ROOM_HEIGHT - 1)
    if random.random() < indpb:
        intensity = random.uniform(0, 1)
    mutated_light = (x, y, intensity)
    print(mutated_light)  # <-- Add this line to check the mutated light
    return mutated_light


# Define the main function
def main():
    # Create the DEAP framework
    creator.create("FitnessMin", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    toolbox.register("light", generate_light)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.light, n=NUM_LIGHTS)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate_fitness)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutate_light, indpb=0.1)
    toolbox.register("select", tools.selNSGA2)

    # Set the random seed
    random.seed(42)

    # Initialize the population
    pop = toolbox.population(n=100)

    # Run the optimization process
    fits = []
    for gen in range(100):
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.5, mutpb=0.5)
        fits += toolbox.map(toolbox.evaluate, offspring)
        for child, fit in zip(offspring, fits):
            child.fitness.values = fit
        pop = toolbox.select(offspring, k=len(pop))

    # Print the best individual
    best_ind = tools.selBest(pop, k=1)[0]
    print("Best individual:", best_ind)

    # Visualize the results
    x = [light[0] for light in best_ind]
    y = [light[1] for light in best_ind]
    intensity = [light[2] for light in best_ind]
    plt.scatter(x, y, s=intensity*1000, alpha=0.5)
    plt.xlim(0, ROOM_WIDTH)
    plt.ylim(0, ROOM_HEIGHT)
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.title("Optimized Light Positions")
    plt.show()

if __name__ == "__main__":
    main()

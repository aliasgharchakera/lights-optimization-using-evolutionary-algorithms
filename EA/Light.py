import random

import os
import sys

# add the parent directory of the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from EA.Problem import Problem
from Lumen.create_room import Room

class Light(Problem):

    # inverse_fitness = True # variable used if we are to generate grpahs S
    

    # CREATE CHROMSONE REPRESENTATION !
    @staticmethod
    def chromosome(room : Room, width, height) -> list:
        """
        Returns:
            list: Returns a chromosome representing a possible solution of lights (grid) in the population
        """
        # Set the minimum and maximum number of lights allowed
        min_lights = 1
        max_lights = width * height // (height) # see if this is to be changed 

        # Generate a random number of lights for this chromosome
        num_lights = random.randint(min_lights, max_lights)

        # Randomly generate the (x, y) positions for each light
        chromosone = []
        # num = room.num_lit_tiles()
        # while num<=width*height*0.7:
        #     # Generate a random position for the light
        #     x = random.randint(0, width-1)
        #     y = random.randint(0, height-1)
        #     chromosone.append((x, y))
        #     # Calculate the number of lit tiles
        #     room.light_light(x, y)
        #     room.light_tiles()
        #     num = room.num_lit_tiles()

        for i in range(num_lights):
            # Generate a random position for the light
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            chromosone.append((x, y))

        # Return the list of light positions (chromosome)
        return chromosone

    @staticmethod
    def fitness_function(Room: Room, light_positions: list, w: float = 0.5) -> float:
        """
        Calculates the fitness of a chromosome based on the number of lit tiles and number of lights in the room.

        Args:
            Room (Room): The room object containing the tile grid and light positions
            light_positions (list): The list of light positions in the chromosome
            w (float, optional): 
                The weight of the number of lit tiles objective in the fitness function. Defaults to 0.5.
                If w is close to 1, then the number of lit tiles will be the dominant factor in determining fitness. 
                If w is close to 0, then the number of lights in the chromosome will be the dominant factor. 
                A value of w at 0.5 means both objectives have equal importance.

        Returns:
            float: The fitness value of the chromosome
        """

        # Calculate the number of lit tiles
        for x,y in light_positions:
            Room.light_light(x, y)

        Room.light_tiles()
        num_lit_tiles = Room.num_lit_tiles()
        # print(num_lit_tiles)

        # Calculate the number of lights in the chromosome
        num_lights = len(light_positions)

        # Calculate the fitness as a weighted sum of the two objectives
        # We want to maximize the number of lit tiles and minimize the number of lights in the chromosome
        fitness = w * num_lit_tiles - (1 - w) * num_lights

        # print("num lit tiles : ",num_lit_tiles," len of chromosone : ", len(light_positions), " fitness: ", fitness)
        
        # Tiles = []
        # Tiles.append(Room.tiles)
        # Reset the room

        tiles = Room.tiles
        Room.reset()

        return fitness, tiles


    # CROSSOVER COMPLETE 
    @staticmethod
    def crossover(parent1: list, parent2: list) -> list:
        """Returns a offspring after breeding from two parents(two list of possible light locations)

        Args:
            parent1 (list): first parent(list of possible ligth positions)
            parent2 (list): second parent(list of possible light positions)

        Returns:
            list: offspring after breeding from two parents
        """

        # select two random genes from parents
        gene1 = int(random.random() * len(parent1))
        gene2 = int(random.random() * len(parent1))

        # find the start and end gene for breeding
        start_gene = min(gene1, gene2)
        end_gene = max(gene1, gene2)

        # create child 1 by taking genes from start_gene to end_gene from parent1
        child1 = parent1[start_gene:end_gene]

        # create child 2 by taking genes not present in child1 from parent2
        child2 = [gene for gene in parent2 if gene not in child1]

        # concatenate child1 and child2 to create the final offspring
        child = child1 + child2
        return child

    # MUTATE COMPLETE 
    @staticmethod
    def mutate(individual: list) -> list:
        """Mutates the positioning of lights by swapping two postions from the list of postions of lightts

        Args:
            individual (list): list of possible light locations

        Returns:
            list: list of possible light locations after mutation
        """

        # select two random indexes to swap in the individual chromosome
        indexes = random.sample(list(range(len(individual))), 2)

         # swap the two chromosones at the selected indexes
        swap1, swap2 = indexes[0], indexes[1]
        individual[swap1], individual[swap2] = individual[swap2], individual[swap1]

        # return mutated choromose
        return individual

# light = Light()
# print(light.chromosome(5,5))
# r=Room(20,20,20,[(0,2,2,0)])
# print(light.fitness_function(r,light.chromosome(5,5)))
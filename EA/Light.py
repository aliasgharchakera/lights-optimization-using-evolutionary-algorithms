import random
from Problem import Problem


from create_room import Room
from lights import Lights
from tiles import Tile

class Light(Problem):

    # inverse_fitness = True # variable used if we are to generate grpahs S

    # CREATE CHROMSONE REPRESENTATION !
    @staticmethod
    def chromosome(width, height) -> list:
        """
        Returns:
            list: Returns a chromosome representing a possible solution of lights (grid) in the population
        """
        # Set the minimum and maximum number of lights allowed
        min_lights = 1
        max_lights = width * height 

        # Generate a random number of lights for this chromosome
        num_lights = random.randint(min_lights, max_lights)

        # Randomly generate the (x, y) positions for each light
        chromosone = []

        for i in range(num_lights):
            # Generate a random position for the light
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            chromosone.append((x, y))

        # Return the list of light positions (chromosome)
        return chromosone

    # CREATE FITNESS FUNCTION 
    @staticmethod
    def fitness_function(light_positions: list) -> float:
        """Calculates the -----

        Args:
            route (list): ----

        Returns:
            float: ----
        """

        length_chromosone = len(light_positions)

        for x,y in light_positions:
            Room.light_light(x, y)
        
        # run, does all claulations
        light_tiles

        # return the actual lit tiles, based on al calulation
            def num_lit_tiles(self):
            
        # divide by chromosone length 
        # 
        give us fitness

        # reset function for room    

  
        return 

    # CROSSOVER COMPLETE 
    @staticmethod
    def crossover(parent1: list, parent2: list) -> list:
        """Returns a offspring after breeding from two parents

        Args:
            parent1 (list): first parent
            parent2 (list): second parent

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
        """Mutates the ----- by swapping two -----

        Args:
            individual (list): list of -----

        Returns:
            list: list of ---- after mutation
        """

        # select two random indexes to swap in the individual chromosome
        indexes = random.sample(list(range(len(individual))), 2)

         # swap the two chromosones at the selected indexes
        swap1, swap2 = indexes[0], indexes[1]
        individual[swap1], individual[swap2] = individual[swap2], individual[swap1]

        # return mutated choromose
        return individual

light = Light()
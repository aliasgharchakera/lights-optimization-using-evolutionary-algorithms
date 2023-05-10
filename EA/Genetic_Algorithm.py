import random

import os
import sys

# add the parent directory of the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importing our abstract Problem class and our selection scheme class
from EA.Problem import Problem
from EA.Selection_schemes import SelectionSchemes
from EA.Light import Light
from Lumen.create_room import Room



# Main Genetic Algorithm Class
class GA:
    
    # Constructor for the initialisation of our GA
    def __init__(
                self,
                problem: Problem,
                X: int,
                Y: int,
                H: int,
                room: Room,
                parent_selection: int = 0,
                survivor_selection: int = 0,
                population_size: int = 30,
                number_of_offsprings: int = 10,
                number_of_generations: int = 100,
                mutation_rate: float = 0.50
                ) -> None:
         
        self.x = X
        self.y = Y
        self.h = H
        self.room = room

        # Initialsing our GA components from specified problem class that will be passed
        self.chromosome = problem.chromosome
        self.fitness_function = problem.fitness_function
        self.mutate = problem.mutate
        self.crossover = problem.crossover

        # Initialising our GA selection schemes,from our Selectionschemes class
        self.selection_schemes = SelectionSchemes(
            fitness_function = problem.fitness_function,
            room=self.room,
            population_size = population_size
            )
        
        """
        selection_methods = [
            self.fitness_proportionate, self.ranked_selection,
            self.tournament_selection, self.truncation, self.random_selection
        ]
        """
        # Initailisng index of selection method to choose from above list of specified selection schemes
        self.parent_selection = parent_selection
        self.survivor_selection = survivor_selection

        # Initialising the rest of our GA characteristics, directly given to GA
        self.population_size = population_size
        self.number_of_offsprings = number_of_offsprings
        self.number_of_generations = number_of_generations
        self.mutation_rate = mutation_rate


    # Define the initial_population function to create an initial population of chromosomes
    def initial_population(self) -> list:
        """Initial population of chromosomes

        Returns:
            list: List of chromosomes of length population_size
        """
        population = []
        for i in range(self.population_size):
            individual = self.chromosome(self.room,self.x, self.y)
            population.append(individual)
        return population

    # Define the get_best_individual function to find the fittest chromosome from the population
    def get_best_individual(self, population: list):
        """Get the fittest chromosome from the population

        Args:
            population (list): List of chromosomes
        """
        # Calculate the fitness of each chromosome in the population
        fitness_values = []
        for chromosome in population:
            fitness, tiles = self.fitness_function(self.room, chromosome)
            fitness_values.append(fitness)
        
        # Find the index of the chromosome with the highest fitness value
        best_fitness_index = fitness_values.index(max(fitness_values))

        # print(best_fitness_index)
        # Return the chromosome with the highest fitness value
        return population[best_fitness_index]
        
        #return max(population, key=self.fitness_function(self.room,population))

    # Define the get_best_fitness function to find the best fitness of the population
    def get_best_fitness(self, population: list) -> float:
            """Get the best fitness of the population

            Args:
                population (list): List of chromosomes

            Returns:
                float: Best fitness of the population
            """
            # Find the best chromosome in the population
            best_chromosome = self.get_best_individual(population)
            # print(best_chromosome)
            # Calculate the fitness of the best chromosome
            return self.fitness_function(self.room,best_chromosome)
            

    # ----------------------------------------- SELECTION SCHEMES ------------------------------------------- #
    
    def truncation(self, population: list) -> list:
        """Truncation selection method

        Args:
            population (list): List of chromosomes

        Returns:
            list: List of chromosomes after truncation
        """
        return self.selection_schemes.truncation(population)

    def fitness_proportionate(self, population: list) -> list:
        """Fitness Propotionate Selection method

        Args:
            population (list): List of chromosomes

        Returns:
            list: List of chromosomes after fitness proportionate selection
        """
        return self.selection_schemes.fitness_proportionate(population)

    def tournament_selection(self, population: list) -> list:
        """Binary Tournament selection method

        Args:
            population (list): List of chromosomes

        Returns:
            list: List of chromosomes after tournament selection
        """
        return self.selection_schemes.tournament_selection(population)

    def ranked_selection(self, population: list) -> list:
        """Ranked based selection method

        Args:
            population (list): List of chromosomes

        Returns:
            list: List of chromosomes after ranked based selection
        """
        return self.selection_schemes.ranked_selection(population)

    def random_selection(self, population: list) -> list:
        """Random selection method

        Args:
            population (list): List of chromosomes

        Returns:
            list: List of chromosomes after random selection
        """
        return self.selection_schemes.random_selection(population)

    # -----------------------------------------        END        ------------------------------------------- #
    
    # Perform crossover and mutation to generate a new offspring given two parents.
    def get_offspring(self, parent1, parent2):
        """Get the offspring of two parents using crossover and mutation

        Args:
            parent1 (_type_): Parent 1
            parent2 (_type_): Parent 2

        Returns:
            _type_: Offspring of parent 1 and parent 2 after crossover and mutation
        """
        child = self.crossover(parent1, parent2)
        if random.random() < self.mutation_rate:
            return self.mutate(child)
        return child

    # Returns a new population of chromosomes generated by breeding the parents given a population of chromosomes
    def breed_parents(self, population: list) -> list:
        """Breed the parents to get the offsprings

        Args:
            population (list): List of chromosomes

        Returns:
            list: List of chromosomes after breeding
        """
        # iterate over number of offspring we want to produce
        for _ in range(self.number_of_offsprings):
            # select 2 random parents from the population
            parents = random.sample(population, 2)
            # breed the parents to get a child chromosome
            child = self.get_offspring(parents[0], parents[1])
            # add the child chromosome to the population
            population.append(child)
        # return the new population of chromosomes
        return population


    # Generate the next population of survivours 
    def next_generation(self, population: list) -> list:
        """Get the next generation using selection methods and breeding of the parents

        Args:
            population (list): List of chromosomes

        Returns:
            list: List of chromosomes after selection and breeding
        """

        # selection_methods is a list of functions to select parents and survivors
        selection_methods = [
            self.fitness_proportionate, self.ranked_selection,
            self.tournament_selection, self.truncation, self.random_selection
        ]

        # parent selection: select parents from population
        parents = selection_methods[self.parent_selection](population)

        # breed parents to create new offsprings and add them to the population
        new_population = self.breed_parents(parents)

        # survivor selection: select survivors from new population
        survivors = selection_methods[self.survivor_selection](new_population)
        return survivors

    # Defines a single step in the evolution to obtain the best fitness of the population.
    def step(self, population: list) -> tuple[list, float]:
        """Get population of generation and best fitness of 
        the population after selection and breeding of the parents

        Args:
            population (list): List of chromosomes

        Returns:
            tuple[list, float]: List of chromosomes after 
            selection and breeding and best fitness of the population
        """
        # print(self.next_generation(population))
        return self.next_generation(population), self.get_best_fitness(population)

    # Runs the evolution, on the num of generations, and return a list of best fitness of the population.
    def run(self) -> list:
        """Run the evolution

        Returns:
            list: List of best fitness of the population
        """
        # Get the initial population
        population = self.initial_population()
        # print(population)

        # print(population)
        # Create a list to store the best fitness value for each generation
        fitness_lst = []
        
        fit_pouplation = []

        fit_tiles = []
        # Iterate over the specified number of generations
        for _ in range(self.number_of_generations):
            
            # Get the next generation by selecting and breeding the parents from the current population
            population, obj = self.step(population)
            best_individual = self.get_best_individual(population)
            
            best_fitness, tiles = obj
            # Append the best fitness value of the current generation to the list
            fitness_lst.append(best_fitness)

            # Appenf the best population of current generation to the list 
            fit_pouplation.append(best_individual)

            fit_tiles.append(tiles)
        
        # Return the list of best fitness values for each generation
        return fitness_lst, fit_pouplation,fit_tiles

"""
selection_methods = [
    self.fitness_proportionate, self.ranked_selection,
    self.tournament_selection, self.truncation, self.random_selection
]
0,0 100,13,43.5
0,1 100,9,45.5
0,2 98,9,44.5
0,3 98,5,46.5
0,4 97,14,41.5

1,0 97,8,44.5
1,1 99,7,46
1,2 99,10,45
1,3 99,8,45.5
1,4 100,11,44.5

2,0 99,8,45.5
2,1 100,9,45.5
2,2 100,8,46
2,3 99,9,45
2,4 98,7,45.5

3,0 98,7,45.5
3,1 97,7,45.5
3,2 99,6,46.5
3,3 99,7,46
3,4 99,7,46

4,0 97,6,45.5
4,1 100,11,44.5
4,2 99,7,46
4,3 100,8,46
4,4 99,13,43

"""
import matplotlib.pyplot as plt

# draw a graph of fitness over generations where the axis are labelled
def draw_graph(fitness, len_population, tiles):
    plt.plot(len_population)
    plt.plot(tiles)
    plt.xlabel('Generation')
    plt.ylabel('Len of Chromosome')
    plt.title('Len of Chromosome over generations')
    plt.show()

if __name__ == "__main__":
    room = Room(100,100,50,[(0,0,2,45),(5,5,2,42),(1,9,2,10),(3,9,1,4)],16, [(0, 3, 15, 15, 8)])
    opt = GA(
        problem=Light,
        X = 10,
        Y = 10,
        H = 50,
        room = room,
        parent_selection = 3,
        survivor_selection = 2,
        population_size=30,
        number_of_offsprings=10,
        number_of_generations=100,
        mutation_rate=0.50
        )

    population = (opt.initial_population())
    fitness, population, tiles = opt.run()
    
    len_num_lit_tiles = []
    
    for p in population:
        for x, y in p:
            room.light_light(x, y)

        room.light_tiles()
        num_lit_tiles = room.num_lit_tiles()
        len_num_lit_tiles.append(num_lit_tiles)
        room.reset()
    
    len_population = [len(p) for p in population]
    draw_graph(fitness, len_population, len_num_lit_tiles)

# fitness, population, tiles= (opt.run())
# print(fitness, "\n",population,"\n", tiles)
# for each in fitness:
#     print (each)

# for each in population:
#     print (each)
#     print()
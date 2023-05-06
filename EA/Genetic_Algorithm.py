import random

# Importing our abstract Problem class and our selection scheme class
from EA.Problem import Problem
from EA.Selection_schemes import SelectionSchemes

# Main Genetic Algorithm Class
class GA:
    # Constructor for the initialisation of our GA
    def __init__(
                self,
                problem: Problem,
                parent_selection: int = 0,
                survivor_selection: int = 0,
                population_size: int = 30,
                number_of_offsprings: int = 10,
                number_of_generations: int = 100,
                mutation_rate: float = 0.50
                ) -> None:

        # Initialising our GA selection schemes,from our Selectionschemes class
        self.selection_schemes = SelectionSchemes(
            population_size=population_size,
            fitness_function=problem.fitness_function
            )

        # Initialsing our GA components from specified problem class that will be passed
        self.chromosome = problem.chromosome
        self.fitness_function = problem.fitness_function
        self.mutate = problem.mutate
        self.crossover = problem.crossover

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
        return [self.chromosome() for _ in range(self.population_size)]

    # Define the get_best_individual function to find the fittest chromosome from the population
    def get_best_individual(self, population: list):
        """Get the fittest chromosome from the population

        Args:
            population (list): List of chromosomes
        """
        return max(population, key=self.fitness_function)

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
            
            # Calculate the fitness of the best chromosome
            return self.fitness_function(best_chromosome)


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
        return self.next_generation(population), self.get_best_fitness(population)

    # Runs the evolution, on the num of generations, and return a list of best fitness of the population.
    def run(self) -> list:
        """Run the evolution

        Returns:
            list: List of best fitness of the population
        """
        # Get the initial population
        population = self.initial_population()
        
        # Create a list to store the best fitness value for each generation
        fitness_lst = []
        
        # Iterate over the specified number of generations
        for _ in range(self.number_of_generations):
            
            # Get the next generation by selecting and breeding the parents from the current population
            population, best_fitness = self.step(population)
            
            # Append the best fitness value of the current generation to the list
            fitness_lst.append(best_fitness)
        
        # Return the list of best fitness values for each generation
        return fitness_lst

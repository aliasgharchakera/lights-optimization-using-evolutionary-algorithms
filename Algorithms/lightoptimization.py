import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import random
from Lumen.tiles import Tile
from Evolution.problem import Problem
from Evolution.selection_schemes import SelectionSchemes

class Chromosome:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.tiles = [[Tile(i, j, 0, 0) for j in range(self.y)] for i in range(self.x)]
        self.generate_tiles()
        
    def generate_tiles(self):
        for i in range(self.x):
            for j in range(self.y):
                self.tiles.append(Tile(i))


class LightOptimization(Problem):
    
    def __init__(self,
                 x: int,
                 y: int,
                 selection_method1: int = 0,
                 selection_method2: int = 0,
                 population_size: int = 30,
                 number_of_offsprings: int = 10,
                 number_of_generations: int = 100,
                 mutation_rate: float = 0.50) -> None:

        self.selection_schemes = SelectionSchemes(
            population_size=population_size,
            fitness_function=self.fitness_function)

        self.selection_method1 = selection_method1
        self.selection_method2 = selection_method2

        self.population_size = population_size
        self.number_of_offsprings = number_of_offsprings
        self.number_of_generations = number_of_generations
        self.mutation_rate = mutation_rate
        
    def initial_population(self) -> list:
        """Initial population of chromosomes

        Returns:
            list: List of chromosomes of length population_size
        """
        return [self.chromosome() for _ in range(self.population_size)]
            
    def chromosome(self):
        """Returns a random route of cities

        Returns:
            list: A random route of cities
        """
        return Chromosome(self.x_tiles, self.y_tiles)

    def fitness_function(route: list) -> float:
        """Calculates the distance covered in the route

        Args:
            route (list): different routes of cities

        Returns:
            float: distance covered in the route
        """
        N = len(graph) - 1
        distances = list(map(lambda x: graph[route[x]][route[x + 1]], range(N)))
        return 1 / sum(distances)

    def mutate(individual: list) -> list:
        """Mutates the route by swapping two cities

        Args:
            individual (list): list of cities

        Returns:
            list: list of cities after mutation
        """
        indexes = random.sample(list(range(len(individual))), 2)
        swap1, swap2 = indexes[0], indexes[1]
        individual[swap1], individual[swap2] = individual[swap2], individual[
            swap1]
        return individual

    def crossover(parent1: list, parent2: list) -> list:
        """Returns a offspring after breeding from two parents

        Args:
            parent1 (list): first parent
            parent2 (list): second parent

        Returns:
            list: offspring after breeding from two parents
        """
        gene1 = int(random.random() * len(parent1))
        gene2 = int(random.random() * len(parent1))

        start_gene = min(gene1, gene2)
        end_gene = max(gene1, gene2)
        child1 = parent1[start_gene:end_gene]
        child2 = [gene for gene in parent2 if gene not in child1]
        child = child1 + child2
        return child

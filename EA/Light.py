import random
from EA.Problem import Problem

class Light(Problem):

    # inverse_fitness = True # variable used if we are to generate grpahs S

    # CREATE CHROMSONE REPRESENTATION !
    @staticmethod
    def chromosome() -> list:
        """Returns a ----

        Returns:
            list: A -----
        """
        return 

    # CREATE FITNESS FUNCTION 
    @staticmethod
    def fitness_function(route: list) -> float:
        """Calculates the -----

        Args:
            route (list): ----

        Returns:
            float: ----
        """
  
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


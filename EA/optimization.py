import matplotlib.pyplot as plt
import pandas as pd

import os, sys
# add the parent directory of the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from EA.Problem import Problem
from EA.Genetic_Algorithm import GA
from EA.Light import Light
from Lumen.create_room import Room


class Optimization:

    def __init__(
        self,
        problem: Problem,
        X: int,
        Y: int,
        H: int,
        room: Room,
        population_size: int = 30,
        number_of_offsprings: int = 10,
        number_of_generations: int = 100,
        mutation_rate: float = 0.50,
        number_of_iterations: int = 10,
        selection_case: tuple = (0, 0)) -> None:
        """Initializes the Optimization class with the given parameters

        Args:
            problem (Problem): Problem class from Evolution.problem
            population_size (int, optional): population size. Defaults to 30.
            number_of_offsprings (int, optional): number of offsprings. Defaults to 10.
            number_of_generations (int, optional): number of generations. Defaults to 100.
            mutation_rate (float, optional): mutation rate. Defaults to 0.50.
            number_of_iterations (int, optional): number of iterations. Defaults to 10.
            selection_case (tuple, optional): selection case. Defaults to (0, 0).
        """
        self.population_size = population_size
        self.number_of_generations = number_of_generations
        self.number_of_iterations = number_of_iterations

        self.number_of_offsprings = number_of_offsprings
        self.problem = problem

        self.mutation_rate = mutation_rate
        self.selection_case = selection_case

        self.x = X
        self.y = Y
        self.h = H
        self.room = room
        
    def evolve(self) -> GA:
        """Returns an Evolution object

        Returns:
            Evolution: Evolution object
        """
        best_fitness = []
        best_population = []
        best_tiles = []
        for time in range(0, 24, 3):
            self.room = Room(100,100,50,[(0,0,2,45),(5,5,2,42),(1,9,2,10),(3,9,1,4)], time, [(0, 3, 15, 15, 8)])
            ga = GA(
                problem=self.problem,
                X = self.x,
                Y = self.y,
                H = self.h,
                room = self.room,
                mutation_rate=self.mutation_rate,
                population_size=self.population_size,
                parent_selection=self.selection_case[0],
                survivor_selection=self.selection_case[1],
                number_of_generations=self.number_of_generations,
                number_of_offsprings=self.number_of_offsprings
                )
            fitness, population, tiles = ga.run()
            # sort fitness, population and tiles according to the best fitness using zip in descending order
            fitness, population, tiles = zip(*sorted(zip(fitness, population, tiles), reverse=True))
            best_fitness.append(fitness[0])
            best_population.append(population[0])
            best_tiles.append(tiles[0])
            
        for i, p in enumerate(best_population):
            for c in p:
                for x, y in c:
                    self.room.light_light(x, y)
                self.room.light_tiles()
            for row in best_tiles[i]:
                for tile in row:
                    print(tile, end = " ")
                print()
            print("Time: ", i*3, "Fitness: ", best_fitness[i])
            self.room.reset()
        
    

    def get_title(self, fitness_type: str) -> str:
        """Returns the title of the plot

        Args:
            fitness_type (str): fitness type (BSF or ASF)

        Returns:
            str: title of the plot 
        """
        selection_cases = ["FPS", "RBS", "Tournament", "Truncation", "Random"]
        title = f"{fitness_type} - {self.problem.__name__} - "
        title += f"{selection_cases[self.selection_case[0]]} &"
        title += f"{selection_cases[self.selection_case[1]]}\n"
        title += f"Pop Size: {self.population_size}; "
        title += f"Num Offsprings: {self.number_of_offsprings}; "
        title += f"Mutation Rate: {self.mutation_rate}"

        return title

    def get_filename(self, fitness_type: str) -> str:
        """Returns the filename of the plot to be saved

        Args:
            fitness_type (str): fitness type (BSF or ASF)

        Returns:
            str: filename of the plot to be saved
        """
        filename = f"{fitness_type}_{self.problem.__name__}"
        filename += f"_{self.selection_case[0]}"
        filename += f"_{self.selection_case[1]}"
        filename += f"_{self.population_size}"
        filename += f"_{self.number_of_offsprings}"

        return filename

    def plot_BSF(self) -> None:
        """Plots the best fitness of the evolution"""
        evolution = self.evolve()
        fitness_lst = evolution.run()

        if self.problem.inverse_fitness:
            fitness_lst = [(1 / fitness) if fitness != 0 else 100
                           for fitness in fitness_lst]

        # print("Initial fitness: ", fitness_lst[0])
        # print("Final fitness: ", fitness_lst[-1])

        x = list(range(len(fitness_lst)))
        y = fitness_lst

        title = self.get_title("Best Fitness")

        plt.title(title)
        plt.plot(x, y)

        filename = self.get_filename("BSF")
        plt.savefig("Analysis/" + filename + ".png")
        plt.close()

    def plot_ASF(self) -> None:
        """Plots the average fitness of the evolution"""
        runs: dict[str, list] = dict()

        for iteration in range(self.number_of_iterations):
            runs["Run #" + str(iteration + 1)] = self.evolve().run()

        df = pd.DataFrame(runs)

        def invert(val):
            if val == 0:
                return 100
            return 1 / val

        df["Average"] = df.mean(axis=1)

        print("Best Average Fitness: ")

        df.index.name = "Generation #"

        title = self.get_title("Average Fitness")

        plt.title(title)
        filename = self.get_filename("ASF")

        if self.problem.inverse_fitness:
            df["Average"] = df["Average"].apply(invert)
            print(df["Average"].min())
        else:
            print(df["Average"].max())

        plt.plot(df["Average"])
        plt.savefig("Analysis/" + filename + ".png")
        plt.close()

opt = Optimization(
    problem=Light,
    X = 10,
    Y = 10,
    H = 10,
    room = None,
    population_size=30,
    number_of_offsprings=10,
    number_of_generations=100,
    mutation_rate=0.50,
    number_of_iterations=10,
    selection_case=(3, 2)
    )

opt.evolve()

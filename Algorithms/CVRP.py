import random
import numpy as np
import math
from input import readFile

class Ant:
    def __init__(self, routes, distance) -> None:
        self.routes = routes
        self.distance = distance

class AntColonyOptimization:
    def __init__(self, alpha, beta, iteration, numAnts, rho, path) -> None:
        self.alpha = alpha
        self.beta = beta
        self.iteration = iteration
        self.numAnts = numAnts
        self.evapRate = 1 - rho
        self.Q = 1

        # Reading the Distance Matrix file with help of ACO File Read
        fileInst = readFile(path)
        self.capacity = fileInst["capacity"]
        self.depot = fileInst["depot"][0]
        self.n = fileInst["dimension"]
        self.demand = fileInst["demand"]
        self.distances = fileInst["edge_weight"]

        self.eta = np.reciprocal(self.distances, out=np.zeros_like(self.distances), where=self.distances!=0)
        self.tau = np.zeros((self.n, self.n))
        self.minDistance = np.inf
        self.minRoute = None
        self.avgDistances = list()


    def AntColonySimulation(self, initialize=False) -> None:
        '''
        Simulates the Ant Colony Optimization Algorithm
        
        Args:
            initialize (bool, optional): If True, we randomly select a path, else we use the pheromones to select the path. Defaults to False
        '''
        # If initialize is True, we randomly select a path, else we use the pheromones to select the path
        self.ants = list()
        for i in range(self.numAnts):
            ant = self.simulateAnt(initialize)
            self.ants.append(ant)

       
    def computeTau(self) -> list[list]:
        '''
        Computes the pheromones for the first iteration
        
        Returns the pheromones
        '''
        deltaTau = np.zeros((self.n, self.n))
        for ant in self.ants:
            for route in ant.routes:
                for path in range(0,len(route)-1):
                    deltaTau[route[path]][route[path + 1]] += np.reciprocal(ant.distance)
                    deltaTau[route[path + 1]][route[path]] += np.reciprocal(ant.distance)
        return deltaTau
    

    def calculateProbabilities(self, currentCity, potentialCities) -> list:
        '''
        Calculates the probabilities of choosing the next city
        
        Returns the list of probabilities
        
        Args:
            currentCity (int): The current city
            potentialCities (list): The list of potential cities
        '''
        probabilities = list()
        for i in potentialCities:
            p = math.pow(self.tau[currentCity][i], self.alpha) + math.pow(self.eta[currentCity][i], self.beta)
            probabilities.append(p)

        probabilities = np.array(probabilities)/np.sum(probabilities)

        # Now making the ranges of Probabilities
        proportionalProbabilities = list()
        start = 0
        for i in range(len(probabilities)):
            # proportionalProbabilities: [(0, end), ..., (start, 1)]
            proportionalProbabilities.append((start , start + probabilities[i]))
            start += probabilities[i]
        
        return proportionalProbabilities


    def getNextCity(self, currentCity, unvisited, truckCapacity) -> int:
        '''
        Returns the next city to visit
        
        Args:
            currentCity (int): The current city
            unvisited (list): The list of unvisited cities
            truckCapacity (int): The current truck capacity
        '''
        potentialCities = list()
        for city in unvisited:
            if self.demand[city] <= truckCapacity and city != currentCity:
                potentialCities.append(city)
        
        proportionalProbabilities = self.calculateProbabilities(currentCity, potentialCities)

        # Choosing the Random number
        p = random.random()
        for city in range(len(proportionalProbabilities)):
            if p >= proportionalProbabilities[city][0] and p < proportionalProbabilities[city][1]:
                nextCity = city
                break
        
        return potentialCities[nextCity]


    def simulateAnt(self, initialize=False) -> Ant:
        # Initializing/Resetting the route
        '''
        Simulates the Ant
        
        Returns the Ant
        
        Args:
            initialize (bool, optional): If True, we randomly select a path, else we use the pheromones to select the path. Defaults to False
        '''
        route = list()
        unvisited = [i for i in range(self.n)]
        # because of probability calculation in getNextCity function we need to remove depot from unvisited cities
        lim = 1
        if initialize:
            unvisited = unvisited[1:]
            lim = 0
        currentCity, truckCapacity = self.depot, self.capacity
        totalDistance = 0
        path = [currentCity]

        while len(unvisited) > lim:
            if initialize:
                # Choosing random city from unvisited cities
                i = random.randint(0, len(unvisited) - 1)
                nextCity = unvisited[i]
                if self.demand[nextCity] > truckCapacity:
                    totalDistance += self.distances[currentCity][self.depot]
                    route.append(path)
                    # Now the path will again go to Depot to make a full route
                    currentCity = self.depot
                    # Resetting the truck capacity
                    truckCapacity = self.capacity
                    path = [self.depot]
            else:
                # Choosing the city with the help of probabilities
                nextCity = self.getNextCity(currentCity, unvisited, truckCapacity)
            truckCapacity -= self.demand[nextCity]
            totalDistance += self.distances[currentCity][nextCity]

            currentCity = nextCity
            path.append(currentCity)
            if initialize:
                unvisited.pop(i)
            else:
                if currentCity == self.depot:
                    truckCapacity = self.capacity
                    route.append(path)
                    path = [self.depot]
                else:
                    unvisited.remove(currentCity)

        # Now the path will again go to Depot to make a full route
        path.append(self.depot)
        totalDistance += self.distances[currentCity][self.depot]
        # Adding the last path to the route
        route.append(path)
        # minDistance and minRoute are used to store the minimum distance and the route so far
        if totalDistance < self.minDistance:
            self.minDistance = totalDistance
            self.minRoute = route
        # avgDistances is used to store the totaldistance of each ant 
        self.avgDistances.append(totalDistance)
        return Ant(route, totalDistance)


    def updateTau(self):
        '''
        Updates the Tau Matrix
        '''
        deltaTau = self.computeTau()
        self.tau = np.array(self.tau) * self.evapRate + np.array(deltaTau)
            

    def run(self):
        '''
        Runs the Ant Colony Optimization Algorithm
        '''
        self.AntColonySimulation(initialize=True)

        # Computing the Tau Matrix
        self.tau = self.computeTau()
        for i in range(self.iteration):
            self.AntColonySimulation(initialize=False)
            # Updating Tau Matrix
            self.updateTau()

        # Checking the minimum distance after the entire process
        minDist = np.inf
        for ant in self.ants:
            if ant.distance < minDist:
                minDist = ant.distance
                minRoute = ant.routes
        
        print(minDist)
        print(minRoute)
        print("Overall Minimum Distance: ", self.minDistance)
        print("Overall Minimum Route: ", self.minRoute)

        
if __name__ == "__main__":
    aco = AntColonyOptimization(4, 4, 50, 30, 0.5, "A-n32-k5")
    aco.run()

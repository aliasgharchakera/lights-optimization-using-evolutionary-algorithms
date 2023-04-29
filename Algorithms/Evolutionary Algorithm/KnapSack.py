import random
import statistics
import matplotlib.pyplot as plt
import selection_scheme as ss

class KnapSack:

    def __init__(self, filepath:str, n:int) -> None:
        '''
        Constructor for class knapsack. Reads the file and populate stuff
        '''
        self.stuff = list()  #(weight, value)
        with open(filepath) as f:
            lines = f.readlines()
            self.num, self.capacity = lines[0].split()
            self.num, self.capacity = int(self.num), int(self.capacity)
            for i in lines[1::]:
                value, weight = i.split()
                self.stuff.append((int(value), int(weight)))
        # print(len(self.stuff))
        self.numItems = len(self.stuff)
        self.population = self.generatePopulation(n)
        # print(self.population)

    def generatePopulation(self,n:int):
        '''
        Generates population for the knapsack problem. 
        '''
        population = dict()
        for i in range(n):
            lstItems = [(0,0) for i in range(self.numItems)]
            weight = 0
            value  = 0
            randomNum = random.randint(0,self.numItems-1)
            selectItem = self.stuff[randomNum]
            while(weight + selectItem[1] <= self.capacity):
                lstItems[randomNum] = selectItem
                weight += selectItem[1]
                value += selectItem[0]
                randomNum = random.randint(0,self.numItems-1)
                selectItem = self.stuff[randomNum]
            population[value] = lstItems
        return population

    def selectParents(self, selectionChoice:str):

        if selectionChoice == 'binaryTournament':
            firstParent = ss.binaryTournament(self.population)
            secondParent = ss.binaryTournament(self.population)

        elif selectionChoice == 'fitnessProportional':
            parents = ss.fitnessProportionalSelection(self.population, 3, True)
            firstParent = parents[0]
            secondParent = parents[1]

        elif selectionChoice == 'rankBase':
            pass

        return firstParent, secondParent

    def crossOver(self):

        parents = self.selectParents('binaryTournament')
        
        firstParent = self.population[parents[0]]
        secondParent = self.population[parents[1]]

        offSpringDetails = self.createOffSpring(firstParent, secondParent, False)
        self.population[offSpringDetails[0]] = offSpringDetails[1]

        offSpringDetails2 = self.createOffSpring(firstParent, secondParent, True)
        self.population[offSpringDetails2[0]] = offSpringDetails2[1]

    def createOffSpring(self, firstParent, secondParent, swap):
        
        offSpring1 = [(0,0) for i in range(self.num)]
        weight1 = 0
        visited = []

        if (swap == True):
            _firstParent = secondParent
            _secondParent = firstParent
        else:
            _firstParent = firstParent
            _secondParent = secondParent

        for i in range(len(firstParent)//2):
            if (_firstParent[i][1] + weight1 <= self.capacity and _firstParent[i] not in visited):
                visited.append(_firstParent[i])
                offSpring1[i] = _firstParent[i]
                weight1 += _firstParent[i][1]

        i = len(firstParent) // 2
        for j in range(len(firstParent)//2):
            if (_secondParent[i+j][1] + weight1 <= self.capacity and _secondParent[i+j] not in visited):
                visited.append(_secondParent[i+j])
                offSpring1[i+j] = _secondParent[i+j]
                weight1 += _secondParent[i+j][1]
        
        for i in range(len(firstParent)//2):
            if (_secondParent[i][1] + weight1 <= self.capacity and _secondParent[i] not in visited):
                visited.append(_secondParent[i])
                offSpring1[i] = _secondParent[i]
                weight1 += _secondParent[i][1]
 
        i = len(firstParent) // 2
        for j in range(len(firstParent)//2):
            if (_firstParent[i+j][1] + weight1 <= self.capacity and _firstParent[i+j] not in visited):
                visited.append(_firstParent[i+j])
                offSpring1[i+j] = _firstParent[i+j]
                weight1 += _firstParent[i+j][1]        

        return weight1, offSpring1

        
    def calculateFitness(self):
        return list(self.population.keys())
        
    def survivalSelection(self, selectionChoice:str):

        if selectionChoice == 'truncation':
            self.population = ss.truncation(self.population,30, True)
        
        elif selectionChoice == 'fitnessProportional':
            pass

        elif selectionChoice == 'rankBase':
            ss.rankBaseSelection(self.population,30, False)
      
    def getFitness(self):
        return list(self.population.keys())
        
def main():
    bruh = KnapSack('f8_l-d_kp_23_10000',30)
    # print(bruh.calculateFitness())
    # bruh.crossOver()
    minlst, avglst, avgminlst, avgavglst = list(), list(), list(), list()
    for iteration in range(1):
        # bruh.generatePopulation(30)
        for generation in range(40):
            for offspring in range(5):
                bruh.crossOver()
            bruh.survivalSelection('rankBase')
            # print('Max: ',max(bruh.getFitness()))
            minlst.append(max(bruh.getFitness()))
            avglst.append(statistics.mean(bruh.getFitness()))
            # print('Avg: ',statistics.mean(bruh.getFitness()))
        avgminlst.append(statistics.mean(minlst))
        avgavglst.append(statistics.mean(avglst))
    return minlst, avglst
    # for i in range(10):
    #     for i in range(1000):
    #         for i in range(5):
    #             bruh.crossOver()
    #         bruh.survivalSelection('truncation')
    # print(bruh.calculateFitness())


minlst, avglst = main()
plt.plot([i for i in range(1, 41)], minlst, label="max")
plt.plot([i for i in range(1, 41)], avglst, label="avg")
plt.xlabel('generation')
plt.title('Plot of average fitness against generations')
# plt.xlabel('iteration')
# plt.title('Plot of average fitness against iterations')
plt.ylabel('fitness')
plt.legend()
plt.show()
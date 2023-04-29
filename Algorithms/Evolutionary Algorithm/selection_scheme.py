
import random

def binaryTournamentSurvival(population:dict, n:int):
    lst = []
    i = 0
    while i < n:
        key = binaryTournament(population)
        if key not in lst:
            lst.append(key)
            i += 1
    newDct = {}
    for i in lst:
        newDct[i] = population[i]
    return newDct

def binaryTournament(population:dict):
    '''
    Selects two parents randomly and selects one which is best
    '''
    lstDctKeys = list(population.keys())
    firstKey = lstDctKeys[random.randint(0,len(lstDctKeys)-1)]
    secondKey = lstDctKeys[random.randint(0,len(lstDctKeys)-1)]
    if (firstKey < secondKey):
        return secondKey
    return firstKey

def truncation(population:dict,n:int, reverse):
    '''
    It will sort the population based on fitness values and truncate the ones with lowest fitness.
    '''
    newDct = {}
    keysLst = list(population.keys())
    if reverse == True:
        keysLst = sorted(keysLst, reverse=True)
    else:
        keysLst.sort()
    lengthOfPopulation = len(keysLst)
    shortListedKeys = list()
    j = 0
    for i in keysLst:
        shortListedKeys.append(i)
        j += 1
        if (j >= n):
            break
    random.shuffle(shortListedKeys)
    for i in shortListedKeys:
        newDct[i] = population[i]
    return newDct


def repairFitnessValues(fitnessValues:list)->list:
    newLst = []
    for i in fitnessValues:
        newLst.append(100000-i)
    return newLst


def fitnessProportionalSelection(population:dict, k, forParents:bool):
    """
    Perform fitness proportional selection on the fitness values.

    :param fitness_values: List of fitness values
    :param k: Number of values to select
    :return: List of selected values
    """
    # Get the total number of values
    newDct = {}
    fitness_values = list(population.keys())
    repaired_fitness_values = repairFitnessValues(fitness_values)
    n = len(fitness_values)

    # Normalize the fitness values
    total_fitness = sum(repaired_fitness_values)
    probabilities = [fitness / total_fitness for fitness in repaired_fitness_values]

    # Select the values based on their probabilities
    selected_values = []
    for i in range(k):
        r = random.random()
        cumulative_probability = 0
        for j in range(n):
            cumulative_probability += probabilities[j]
            if cumulative_probability >= r:
                selected_values.append(fitness_values[j])
                break
            if (len(selected_values)>1 and forParents == True):
                return selected_values

    for i in selected_values:
        newDct[i] = population[i]

    return newDct

def rankBaseSelection(population: dict, k:int, forParents: bool):
    """
    Perform rank-based selection on the fitness values.

    :param fitness_values: List of fitness values
    :param k: Number of values to select
    :return: List of selected values
    """
    # Get the total number of values
    newDct = {}
    fitness_values = list(population.keys())
    repaired_fitness_values = repairFitnessValues(fitness_values)
    n = len(fitness_values)

    # Create a list of tuples, where each tuple contains a value and its rank
    values_with_ranks = list(zip(repaired_fitness_values, range(1, n + 1)))

    # Sort the values in ascending order
    values_with_ranks.sort(key=lambda x: x[0])

    # Create a list of probabilities, where each probability is proportional to its rank
    probabilities = [2 * (n - rank + 1) / (n * (n + 1)) for (value, rank) in values_with_ranks]

    # Select the values based on their probabilities
    selected_values = []
    for i in range(k):
        r = random.random()
        cumulative_probability = 0
        for j in range(n):
            cumulative_probability += probabilities[j]
            if cumulative_probability >= r:
                selected_values.append(fitness_values[j])
                break
            if (len(selected_values) > 1 and forParents == True):
                return selected_values

    for i in selected_values:
        newDct[i] = population[i]
    
    return newDct


def randomSelection(population:dict,k:int):

    lstKeys = list(population.keys())
    length = len(lstKeys) 
    selectedLst = []
    for i in range(k):
        selectedLst.append(lstKeys[random.randint(0,length-1)])
    
    if (k == 2):
        return selectedLst

    newDct = dict()
    for i in selectedLst:
        newDct[i] = population[i]
    return newDct


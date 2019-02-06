#!/usr/bin/env python
# coding: utf-8

# In[1]:


# generating 1 bar of music
# each bar has 5 divisions and each division has 4 quarter notes
# quarter note takes 4 spaces
# one eight note takes 2 spaces
# one sixteenth takes 1 space
import numpy as np
import pandas as pd
import random

"""
class Individual:
    rank = 0
    def __init__(self, arr, fitnessScore):
        #self.id = id
        self.arr = arr
        self.fitnessScore = fitnessScore
"""

def randomspace (availableSpaces):
    if availableSpaces==1:
        return 1
    elif availableSpaces==2 or availableSpaces==3:
        return np.random.choice(
            [2, 1],
            1,
            p=[0.85, 0.15]
        )[0]
    else:
        return np.random.choice(
            [4, 2, 1],
            1,
            p=[0.7, 0.25, 0.05]
        )[0]

def generateIndividual():
    arr = []
    spacearr = []
    for j in range(5):
        division= []
        divisionSpaces = []
        note = -1
        lower = 0
        upper = 24
        spaces = 16
        while spaces > 0:
            spaceForNote = randomspace(spaces)
            divisionSpaces.append(spaceForNote)
            spaces -= spaceForNote
            if note != -1:
                lower = max((note-12), 0)
                upper = min((note+12), 24)
            note = random.randint(lower, upper)
            division.append(note)
            for i in range(spaceForNote-1):
                division.append(-2)
        arr.append(division)
        spacearr.append(divisionSpaces)
    return arr
def fitnessfunction(note1, note2):
    diff= (note2-note1)%13
    if diff == 0: #UNISON
        return 8
    elif diff == 5: #Perfect Fourth
        return 15
    elif diff == 7: #Perfect Fifth
        return 15
    elif diff == 12: #Perfect Octave
        return 8
    elif diff == 4: #Major Third
        return 8
    elif diff == 9: #Major Sixth
        return 8
    elif diff: #Minor Third
        return 8
    elif diff: #Minor Sixth
        return 8
    elif diff == 1: #Minor Second
        return -20
    elif diff == 2: #Major Second
        return -20
    elif diff == 10: #Minor Seventh
        return -20
    elif diff == 11: #Major Sixth
        return -20
    elif diff == 6: #Augmented Diminished
        return -30
    else:
        return 0


#Step 1: generating population

initpop = 10
pop = []
spacepop = []
for j in range(initpop):
    temp = generateIndividual()
    print(temp)
    pop.append(temp)
#print(pop)
#print(spacepop)
#
#Step 2: calculate fitness score
ind = pd.DataFrame(columns = ['comp','fscore'])
#fitPopulation = 10
for i in range(initpop):
    fitness = 0
    for k in range(0, 5):
        division = pop[i][k]
        val1 = division[0]
        j = 1
        while j < 16:
            while j < 16 and division[j] == -2:
                j += 1
            if j < 16:
                val2 = division[j]
                fitness += fitnessfunction(val1, val2)
                val1 = val2
                j += 1
    if fitness > 0:
        ind.loc[ind.shape[0]] = [pop[i], fitness]
print(ind)

for rep in range(2):
    #sorting in ascending order
    ind = ind.sort_values('fscore').reset_index(drop = True)
    print(ind)

    #Step 3: creating new population
    #3.1: using selection
    rank = []
    # assigning ranks based on fitness score
    # lowest 1 gets added to the rank arr once, ..
    for i in ind.index:
        for j in range(i+1):
            rank.append(i)
    parent1 = np.random.choice(rank, 1)[0]
    for i in ind.index:
        if i != parent1:
            for j in range(i+1):
                rank.append(i)
    parent2 = np.random.choice(rank, 1)[0]

    print("Parent1: {} Parent2: {}\n".format(parent1, parent2))

    count = 0;
    #crossover
    while count<4:
        crossoverPoint = np.random.choice([0, 1, 2, 3, 4], 1)[0]
        print(crossoverPoint)
        child = []
        child.append(ind['comp'][parent1][0:crossoverPoint] + ind['comp'][parent2][crossoverPoint:])
        child.append(ind['comp'][parent2][0:crossoverPoint] + ind['comp'][parent1][crossoverPoint:])
        print('parents')
        print(ind['comp'][parent1])
        print(ind['comp'][parent2])
        print('children')
        print(child[0])
        print(child[1])

        #loo for both children

        #mutation
        for ch in range(2):
            individual = child[ch]
            print(child[ch])
            division = random.randint(0, 4)
            print('division is {}'.format(division))
            notePosition = random.randint(0, 13)
            while notePosition < 13 and individual[division][notePosition] == -2:
                notePosition += 1
            print('noteposition {}'.format(notePosition))

            #finding note previous to that
            i = notePosition - 1
            while i >= 0 and individual[division][i] == -2:
                i -= 1
            if i == -1:
                lower = 0
            else:
                lower = i
            print('lower note value {}'.format(lower))
            lowerMin = max(individual[division][lower]-12, 0)
            lowerMax = min(individual[division][lower]+12, 24)
            #finding note after that
            i = notePosition + 1
            while i < 16 and individual[division][i] == -2:
                i += 1
            if i == 16:
                upper = notePosition
            else:
                upper = i
            print('upper note value {}'.format(upper))
            upperMin = max(individual[division][upper]-12, 0)
            upperMax = min(individual[division][upper]+12, 24)

            a = list(range(lowerMin, lowerMax))
            b = list(range(upperMin, upperMax))
            available = a and b
            inter = list(available)
            note = np.random.choice(inter, 1)[0]
            individual[division][notePosition] = note
            print(individual)

            #fitness score for children
            for k in range(0, 5):
                division = individual[k]
                val1 = division[0]
                j = 1
                while j < 16:
                    while j < 16 and division[j] == -2:
                        j += 1
                    if j < 16:
                        val2 = division[j]
                        fitness += fitnessfunction(val1, val2)
                        val1 = val2
                        j += 1
            if fitness >= ind['fscore'][parent1] or fitness >= ind['fscore'][parent1]:
                ind.loc[ind.shape[0]] = [individual, fitness]
                count += 1
            if count>=4:
                break
    ind = ind.sort_values('fscore').reset_index(drop = True)
    quart = np.percentile(ind['fscore'], 50)
    print(quart)
    ind = ind[ind['fscore'] >= quart]
    print(ind)


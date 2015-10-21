import random
import copy

def constructListFromPairs(list):
    actualList = []
    for pair in list:
        numOfVal = pair[1]
        for i in range (numOfVal):
            actualList.append(pair[0])
    return actualList
    
class Gene:
    def __init__(self, list):
        seen = []
        listData = []
        #in order to facilitate proper crossover, it will be necessary to
        #store lists as a list of tuples : with the number of occurrences
        #of each value stored in the format (val, numOfVal).
        for val in list:
            if(val in seen):
                continue
            else:
                seen.append(val)
                valCount = 0
                for num in list:
                    if (num == val):
                        valCount += 1
                listData.append((val,valCount))
                
        self.__listData = listData
        self.fitnessIntMin = 0
        self.fitnessIntMax = 0
        self.fitness = 0
        
    def getFitnessIntMin(self):
        return self.fitnessIntMin
        
    def getFitnessIntMax(self):
        return self.fitnessIntMax
        
    def setFitnessInterval(self, begin, totalFitness):
        self.fitnessIntMin = begin
        range = self.fitness / totalFitness
        self.fitnessIntMax = begin + range
        
    def isSameList(self,other):
        for val in self.__listData:
            if(val not in other.getListData):
                return false
        return true
                
    def sortedNess(self):
        previous = self.__listData[0]
        sortedLength = 0
        for val in self.__listData:
            if(val[0] >= previous[0]):
                sortedLength+=1
                previous = val
        self.fitness = sortedLength / len(self.__listData)
        return self.fitness
        
    def crossover(self, other):
        splitAt = random.randint(1,len(self.__listData)-1)
        #deepcopy is needed so we don't mutate the parents
        otherList = copy.deepcopy(other.getListData())
        selfFront = self.__listData[:splitAt]
        otherFront = otherList[:splitAt]
        selfRest = copy.deepcopy(self.__listData)
        otherRest = otherList
        
        #We will append the two lists by removing duplicates from the other
        #This ensures we retain all values.
        for val in selfFront:
            otherRest.remove(val)
        for val in otherFront:
            selfRest.remove(val)
        
        child1 = Gene(constructListFromPairs( selfFront + otherRest))
        child2 = Gene(constructListFromPairs( otherFront + selfRest))
        print("SplitAt: ",splitAt)
        return child1, child2

    def getListData(self):
        return self.__listData
    
    def constructList(self):
        return constructListFromPairs(self.__listData)
        
    def shuffle(self):
        newOrder = []
        while(self.__listData != []):
            toPick = random.randint(0,len(self.__listData)-1)
            newOrder.append(self.__listData[toPick])
            self.__listData.remove(self.__listData[toPick])
        self.__listData = newOrder
        
    def mutate(self):
        swap1 = random.randint(0,len(self.__listData)-1)
        swap2 = random.randint(0,len(self.__listData)-1)
        temp = self.__listData[swap1]
        self.__listData[swap1] = self.__listData[swap2]
        self.__listData[swap2] = temp
        print("Mutation!")
        
def generateProgeny(population):
    newPop = []
    popSize = len(population)
    while( len(newPop) < popSize):
        toChoose = random.randint(0, 999)
        toChoose /= 1000
        picked1 = None
        picked2 = None
        print("toChoose=",toChoose)
        while(picked1 == picked2):
            toChoose2 = random.randint(0, 999)
            toChoose2 /= 1000
            print("toChoose2=",toChoose2)
            for gene in population:
                if(picked1 == None and toChoose >= gene.getFitnessIntMin() and toChoose <= gene.getFitnessIntMax()):
                    picked1 = gene
                if(toChoose2 >= gene.getFitnessIntMin() and toChoose2 <= gene.getFitnessIntMax()):
                    picked2 = gene
        child1, child2 = picked1.crossover(picked2)
        newPop.append(child1)
        if(len(newPop) != popSize):
            newPop.append(child2)
    if(random.randint(0,1)):
        newPop[random.randint(0,popSize-1)].mutate()
    return newPop
        
def debugAlgorithm(population,maxFit,avgFit):
    for gene in population:
        print(gene.getListData(),gene.fitness,gene.getFitnessIntMin(),gene.getFitnessIntMax())
    print("Avg Fitness=",avgFit)
    print("Max Fitness=",maxFit)

def DarwinSort(list):
    population = []
    popSize = len(list)
    OGene = Gene(list)
    for i in range (popSize-1):
        newGene = copy.deepcopy(OGene)
        newGene.shuffle()
        population.append(newGene)
    population.append(OGene)
    
    maxFitness = 0
    totalFitness = 0
    theBest = None
    for gene in population:
        geneFit = gene.sortedNess()
        if(geneFit >= maxFitness):
            maxFitness = geneFit
            theBest = gene
        totalFitness += geneFit
    avgFit = totalFitness / popSize
        
    while(maxFitness != 1):
        maxFitness = 0
        totalFitness = 0
        theBest = None
        for gene in population:
            geneFit = gene.sortedNess()
            if(geneFit >= maxFitness):
                maxFitness = geneFit
                theBest = gene
            totalFitness += geneFit
        avgFit = totalFitness / popSize
        if(maxFitness == 1):
            break
        #The next few blocks handles generating children
        startAt = 0
        for gene in population:
            gene.setFitnessInterval(startAt,totalFitness)
            startAt = gene.getFitnessIntMax()
        debugAlgorithm(population,maxFitness,avgFit)
        population = generateProgeny(population)
        print("Avg Fitness =", avgFit)
        print("Max Fitness =", maxFitness)
        
    return theBest.constructList()
        
        
            
    
    
        
        
def main():
    print(DarwinSort([24,3,4,32,0,2,2,2,1,0,-1,-33]))
    
main()
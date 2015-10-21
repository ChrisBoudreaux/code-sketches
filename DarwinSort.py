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
        
def generateProgeny(population):
    newPop = []
    popSize = len(population)
    while( len(newPop) < popSize):
        toChoose = random.randint(0, 1000)
        toChoose /= 1000
        toChoose2 = random.randint(0, 1000)
        toChoose2 /= 1000
        picked1 = None
        picked2 = None
        while(picked1 == picked2):
            for gene in population:
                if(toChoose >= gene.getFitnessIntMin() && toChoose <= gene.getFitnessIntMax()):
                    picked1 = gene
                if(toChoose2 >= gene.getFitnessIntMin() && toChoose2 <= gene.getFitnessIntMax()):
                    picked2 = gene
            

def DarwinSort(list):
    population = []
    popSize = len(list)
    OGene = Gene(list)
    for i in range (popSize):
        newGene = copy.deepcopy(OGene)
        newGene.shuffle()
        population.append(newGene)
        
    while(maxFitness != 1):
        maxFitness = 0
        totalFitness = 0
        theBest = None
        for gene in population:
            geneFit = gene.sortedNess
            if(geneFit >= maxFitness):
                matFitness = geneFit
                theBest = gene
            totalFitness += geneFit
        avgFit = totalFitness / popSize
        if(maxFitness == 1):
            break
        #The next few blocks handles generating children
        startAt = 0
        for gene in population:
            gene.setFitnessInterval(startAt,totalFitness)
            startAt = gene.getFitnessIntMax
        
        
            
    
    
        
        
def main():
    myGene = Gene([8,7,6,5,4,3,2,1])
    otherGene = copy.deepcopy(myGene)
    otherGene.shuffle()
    print(myGene.getListData())
    print(otherGene.getListData())
    
main()
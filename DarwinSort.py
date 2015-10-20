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
        return sortedLength / len(self.__listData)
        
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
        
        
def main():
    myGene = Gene([8,7,6,5,4,3,2,1])
    otherGene = Gene([5,2,3,1,8,7,6,4])    
    child1, child2 = myGene.crossover(otherGene)
    print(myGene.getListData())
    print(otherGene.getListData())
    print(child1.getListData())
    print(child2.getListData())
    
main()
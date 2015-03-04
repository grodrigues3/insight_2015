#!/usr/bin/python

import heapq, pdb
from numpy import median, random

class MedianKeeper:
    def __init__(self):
        self.lCount = 0
        self.hCount = 0

        self.h_low = [] #a max heap of the n/2 lowest numbers 
        self.h_high = [] #a min heap of the n/2 highest numbers

    def get_median(self):
        numElements = self.hCount + self.lCount
        if numElements %2 == 0:
            return (self.h_low[0]*(-1) + self.h_high[0])/2.0
        elif self.hCount > self.lCount:
            return self.h_high[0]
        else:
            return self.h_low[0]*-1


    def _add_to_low(self, newElement):
        #print 'adding the low'
        heapq.heappush(self.h_low, -1*newElement)
        self.lCount +=1

    def _add_to_high(self, newElement):
        #print 'adding the high'
        heapq.heappush(self.h_high, newElement)
        self.hCount +=1
        

    def add_element(self, newElement):
        #print "adding {0} to the list".format(newElement)
        loMax = hiMin = None
        if self.lCount >0:
            loMax = -1*self.h_low[0] #the max element of the lower half
        if self.hCount >0:
            hiMin = self.h_high[0] #the min element of the upper half

        if loMax ==None and hiMin == None: #both are empty
            self._add_to_low(newElement)
            return
        #they cannot both be empty
        if loMax:
            if newElement < loMax:
                self._add_to_low(newElement)
            else:
                self._add_to_high(newElement)
        else:
            if newElement >= hiMin:
                self._add_to_high(newElement)
            else:
                self._add_to_low(newElement)
        self.balance()
            

    def balance(self):
        if self.lCount >= self.hCount + 2: #get the biggest from the smallheap and add it to the big one (flip the sign first)
            elementToMove = heapq.heappop(self.h_low) * -1 
            self.lCount -=1
            self._add_to_high(elementToMove)
        elif self.hCount >= self.lCount +2:
            elementToMove = heapq.heappop(self.h_high) 
            self.hCount -=1
            self._add_to_low(elementToMove)

        
         

def test(testValues):
    m = MedianKeeper()
    errors = 0
    for i,value in enumerate(testValues):
        m.add_element(value)
        my_median = m.get_median()
        np_median = median(testValues[:i+1])
        try:
            assert(my_median == np_median)
        except:
            errors +=1
    print "Testing Complete With {0} Errors\n".format(errors), "-"*30

if __name__ == "__main__":
    test_0 = [4,5,4,5]
    test_1 = range(100)
    test_2 = random.randint(-100, 100, 1000)

    test(test_0)
    test(test_1)
    test(test_2)




    

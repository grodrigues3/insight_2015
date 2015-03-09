#!/usr/bin/python
"""

Insight Data Engineering Coding Challenge
The second part of the coding challenge is to implement a method of
easily keeping track of the median of a (streaming) list of elements being passed in.
"""

__author__ = 'grodrigues'

###############################################

import heapq, pdb
import sys
import os
from numpy import median

class MedianKeeper:
    """
    A class that can be use to keep track of the median of a streaming input of numbers
    It works using two heaps as described in numerous algorithms textbooks and in the coursera
    Introduction to Algorithms Course.

    Let n be the number of elements we've seen so far

    1. The first heap is a max heap and contains the n/2 smallest elements.
    2. The second heap is a min heap and contains the n/2 largest elements

    Whenever we add a new element, we add it the heap it belongs to and we rebalance
    the two heaps so that they each have half of the elements seen  (half+1 if the n is odd)
    
    USAGE:
        get_median: returns the median so far
        add_element(someNum): adds a number to one of the two heaps

    """
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
        self._balance()
            

    def _balance(self):
        """
        We only rebalance if one of the two heaps has 2 or more elements than the other
        """
        if self.lCount >= self.hCount + 2: 
            elementToMove = heapq.heappop(self.h_low) * -1 
            self.lCount -=1
            self._add_to_high(elementToMove)
        elif self.hCount >= self.lCount +2:
            elementToMove = heapq.heappop(self.h_high) 
            self.hCount -=1
            self._add_to_low(elementToMove)

        
         

def get_median_for_files(input_dir, output_file):
    print "Calculating the median words per line for all files in {0}".format(input_dir)
    try:
        input_files = os.listdir(input_dir)
        print "\t{0} files are going to be used in the median line length calculation".format(len(input_files))
        print"\t Writing the output to {0} ".format(output_file)
        with open(output_file, 'w') as outFile:
            orderedFiles = sorted(input_files)
            M = MedianKeeper()
            for filename in orderedFiles:
                try:
                    with open(input_dir+filename) as f:
                        for line in f:
                            numWords = len(line.split())
                            M.add_element(numWords)
                            myMed = M.get_median()
                            outFile.write(str(myMed) + "\n")
                except:
                    print "When calculating running median, couldn't open the file: {0}. Proceeding with remaining files".format(filename)

    except:
        import traceback
        traceback.print_exc()
        print "Median ERROR: couldn't access the input directory provided"
        exit(0)


if __name__ == "__main__":
    inputArgs = sys.argv

    if len(inputArgs) < 3:
        print "Warning: Either an input directory (e.g ./wc_input) or an output file (e.g. ./wc_output/wc_result.txt) was not specified."
        print "Using the default values instead"
        input_dir = './wc_input/'
        output_file = "./wc_output/med_result.txt"
    else:
        input_dir = inputArgs[1]
        output_file = inputArgs[2]
    get_median_for_files(input_dir, output_file)



    

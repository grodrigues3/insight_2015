#!/usr/bin/python

"""
Insight Data Engineering Coding Challenge
The first part of the coding challenge is to implement your own version of Word Count that counts all the words from the text files contained in a directory named wc_input and outputs the counts to a file named wc_result.txt,which is placed in a directory named wc_output.
"""

__author__ = 'grodrigues'

import multiprocessing as mp
from collections import defaultdict
from os import listdir
from time import time
import pdb
import sys


""" CONSTANTS """
input_dir = './wc_input/'
testDir = '/home/garrett/msproj/data/tenK/abstracts/'
NUMPROCESSORS = mp.cpu_count() #4 on my computer
test = True


def serial_count(input_directory, printFreq=0):
    print "Counting the words in each document serially..."
    try:
        g = listdir(input_directory)
    except:
        print "Could not access the input directory (wc_input).\n Exiting."
        exit(0)
    trueDict = defaultdict(lambda: 0)
    for i,fn in enumerate(g):
        with open(testDir+fn) as f:
            for line in f:
                words = line.lower().split()
                for word in words:
                    trueDict[word] +=1
        if printFreq and i%printFreq == 0 and i !=0:
            print "Doc Count: {0} \t Elapsed Time: {1}".format(i, time() - start)
    print "Doc Count: {0} \t Elapsed Time: {1}".format(i, time() - start)
    return trueDict

def count_parallel(docs):
    wordCounts = {}
    for doc in docs:
        with open(testDir + doc) as f:
            for line in f:
                words = line.lower().split()
                for word in words:
                    if word in wordCounts:
                        wordCounts[word] +=1
                    else:
                        wordCounts[word] = 1
    return wordCounts

def merge_count_dictionaries(list_of_count_dictionaries):
    trueDict = defaultdict(lambda: 0)
    for wordCountDict in list_of_count_dictionaries:
        for word in wordCountDict:
            trueDict[word] += wordCountDict[word]
    return trueDict

def parallel_count(input_directory):
    print "Counting the words in each document in parallel..."
    g = listdir(input_directory)
    total_files = len(g)
    files_per = total_files*1. / NUMPROCESSORS
    in_args = [g[int(i*files_per):int((i+1)*files_per)] for i in range(NUMPROCESSORS)]
    multi_pool = mp.Pool(processes = NUMPROCESSORS) #use 4 processes for now
    word_counts_by_doc = multi_pool.map(count_parallel, in_args)
    print len(word_counts_by_doc), ' is the number of dictionaries used'
    return merge_count_dictionaries(word_counts_by_doc)
    


if __name__ == "__main__":
    inArgs = sys.argv
    if len(inArgs)>1 and inArgs[1] == 'par':
        start = time()
        parWordCount = parallel_count(testDir)
        end = time()
        print end - start, 'total time elapsed for parallel processing'
    
    start = time()
    wordCounts = serial_count(testDir, printFreq = 10**3)
    end = time()
    print end - start, 'total time elapsed for serial processing'

    try:
        print  len(wordCounts), len(parWordCount)
    except:
        pass


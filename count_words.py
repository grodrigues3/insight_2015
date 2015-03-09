#!/usr/bin/python

"""
2015 Insight Data Engineering Coding Challenge
The first part of the coding challenge is to implement your own version of Word 
Count that counts all the words from the text files contained in a directory
named wc_input and outputs the counts to a file named wc_result.txt,which is 
placed in a directory named wc_output.
"""

__author__ = 'grodrigues'

###############################################
import multiprocessing as mp
from collections import defaultdict
from os import listdir
from time import time
import pdb
import sys

###############################################
""" CONSTANTS """
NUMPROCESSORS = mp.cpu_count() #4 on my computer


### 1. Perform the Word Counting Serially
###############################################
def serial_count(input_directory, printFreq=0):
    print "Counting the words in each document serially..."
    try:
        g = listdir(input_directory)
    except:
        print "Could not access the input directory (wc_input).\n Exiting."
        exit(0)
    trueDict = defaultdict(lambda: 0)
    for i,fn in enumerate(g):
        with open(input_directory+fn) as f:
            for line in f:
                words = line.lower().split()
                for word in words:
                    trueDict[word] +=1
        if printFreq and i%printFreq == 0 and i !=0:
            print "Doc Count: {0} \t Elapsed Time: {1}".format(i, time() - start)
    print "Doc Count: {0} \t Elapsed Time: {1}".format(i, time() - start)
    return trueDict

###2. Perform the Word Counting In Parallel
###############################################


def parallel_count(input_directory):
    print "Counting the words in each document in parallel..."
    g = listdir(input_directory)
    total_files = len(g)
    files_per = total_files*1. / NUMPROCESSORS
    inArgs = []
    for i in range(NUMPROCESSORS):
        inArgs += [(input_directory, g[int(i*files_per):int((i+1)*files_per)])]
    multi_pool = mp.Pool(processes = NUMPROCESSORS) #use 4 processes for now
    word_counts_by_doc = multi_pool.map(count_parallel, inArgs)
    return merge_count_dictionaries(word_counts_by_doc)
    

def count_parallel(dir_and_docs):
    """
    Counts the words only for the specified docs
    dir_and_docs: (input directory, the documents to be processed)
    """
    input_directory, docs = dir_and_docs
    wordCounts = {}
    for doc in docs:
        with open(input_directory + doc) as f:
            for line in f:
                words = line.lower().split()
                for word in words:
                    if word in wordCounts:
                        wordCounts[word] +=1
                    else:
                        wordCounts[word] = 1
    return wordCounts


def merge_count_dictionaries(list_of_count_dictionaries):
    """
    Given a list of dictionaries each containing word counts in the format {word: count...}
    output a single dictionary with each of the counts
    @param list_of_count_dictionaries: list of word count dictionaries

    """
    trueDict = defaultdict(lambda: 0)
    for wordCountDict in list_of_count_dictionaries:
        for word in wordCountDict:
            trueDict[word] += wordCountDict[word]
    return trueDict

### 3. Write to File
###############################################

def write_to_file(countDict, output_filename="./wc_output/wc_result.txt"):
    """
    @param countDict: a dictinary containing the word-> count mappings
    @param output_filename: the name of the file to be written to
    """
    with open(output_filename, 'w') as f:
        for word in sorted(countDict):
            f.write("{0}\t{1}\n".format(word, countDict[word]) )

if __name__ == "__main__":
    inputArgs = sys.argv
    if len(inputArgs) <= 1:
        print "ERROR: Please supply both an input directory (e.g ./wc_input) and an output file (e.g. ./wc_output/wc_result.txt)"
        exit(0)

    input_dir = inputArgs[1]
    output_file = inputArgs[2]

    if "-s" in inputArgs:
        wordCounts = serial_count(input_dir, printFreq = 10**3)
    else:
        wordCounts = parallel_count(input_dir)
    
    write_to_file(wordCounts)


#!/usr/bin/env python
# merge invariant files (text format)

import os
import sys

def loadInvariantToDict(fileName):
    #print 'Loading Invariants from file: ' + fileName
    if not os.path.exists(fileName):
        exit(1)

    f = open(fileName)
    data = {}
    new_ppt = False
    ppt = None
    while True:
        line = f.readline()
        if line == '': # end of file
            break
        elif line == '\n':
            continue
        elif line.startswith("==="): # new program point
            new_ppt = True
        else:
            if new_ppt:
                new_ppt = False
                ppt = line.rstrip("\n\r")
                data[ppt] = set() 
            else:
                if ppt:
                    data[ppt].add(line.rstrip("\n\r"))
    f.close()
    return data

#Merge data2 into data1
def mergeInvs(data1, data2):
    for ppt in data2:
        if ppt in data1:
            for inv in data2[ppt]:
                data1[ppt].add(inv)
        else:
            data1[ppt] = data2[ppt]

def printInvs(data):
    print str(len(data.keys())) + ' Program Points'
    for ppt in data:
        print '=' * 75
        print ppt
        for inv in data[ppt]:
            print inv


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: ' + os.path.basename(sys.argv[0]) + ' InvariantFile1 InvariantFile2 [BuggyInvariantFile3...]'
        exit(1)
    if not os.path.isfile(sys.argv[1]):
        print sys.argv[1] + ' is not a file!'
        exit(1)
    if not os.path.isfile(sys.argv[2]):
        print sys.argv[2] + ' is not a file!'
        exit(1)
    
    invs = loadInvariantToDict(sys.argv[1])
    data = {}

    for fileName in sys.argv[2:]:
        mergeInvs(invs, loadInvariantToDict(fileName))

    printInvs(invs)
# compare two Daikon invariant files (text format)

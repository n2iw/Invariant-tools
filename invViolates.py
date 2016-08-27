#!/usr/bin/env python
# compare two Daikon invariant files (text format)
# output all invariants a buggy version violates

import os
import sys

def loadInvariantToArrays(fileName):
    #print 'Loading Invariants from file: ' + fileName
    if not os.path.exists(fileName):
        exit(1)
    f = open(fileName)
    data = []
    ppts = []
    index = -1
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
            index += 1
        else:
            if new_ppt:
                new_ppt = False
                ppt = line.rstrip("\n\r")
                ppts.append(ppt)
                data.append([])
            else:
                if ppt:
                    data[index].append(line.rstrip("\n\r"))
    f.close()
    return (ppts, data)

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

def printInvs(data):
    #print str(len(data.keys())) + ' Program Points'
    for ppt in data:
        print '=' * 75
        print ppt
        for inv in data[ppt]:
            print inv

def compareInvs(data1, data2):
    data1_only = {}
    data2_only = {}
    both = {}
    for ppt in data2:
        if ppt in data1:
            intersect = data1[ppt] & data2[ppt]
            if intersect:
                both[ppt] = intersect

            d1_only = data1[ppt] - data2[ppt]
            if d1_only:
                data1_only[ppt] = d1_only

            d2_only = data2[ppt] - data1[ppt]
            if d2_only:
                data2_only[ppt] = d2_only

            #if len(d1_only):
            #    print ppt
            #    print '  has ' + str(len(d1_only)) + '/' + str(len(data1[ppt])) + ' unique invariants'
        elif data2[ppt]:
            data2_only[ppt] = data2[ppt]
    return (data1_only, data2_only, both)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: ' + os.path.basename(sys.argv[0]) + ' FixedVersionInvariantFile BuggyInvariantFile1'
        exit(1)
    if not os.path.isfile(sys.argv[1]):
        print sys.argv[1] + ' is not a file!'
        exit(1)
    if not os.path.isfile(sys.argv[2]):
        print sys.argv[2] + ' is not a file!'
        exit(1)
    
    inv1 = loadInvariantToDict(sys.argv[1])
    inv2 = loadInvariantToDict(sys.argv[2])
    
    (inv1_only, inv2_only, both) = compareInvs(inv1, inv2)

    printInvs(inv1_only)

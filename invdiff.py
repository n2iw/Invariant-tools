#!/usr/bin/env python
# compare two Daikon invariant files (text format)

import os
import sys

def loadInvariant(fileName):
    #print 'Loading Invariants from file: ' + fileName
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
                data[ppt].add(line.rstrip("\n\r"))
    f.close()
    return data

def printInv(data):
    print str(len(data.keys())) + ' Program Points'
    for ppt in data:
        print '=' * 80
        print ppt
        for inv in data[ppt]:
            print '  ' + inv

# data1 is the invariant file for bug-free version 
# data2 is the invariant file for buggy version
# only compare Program Points that exits in both data1 and data2
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

            if len(d1_only):
                print ppt
                print '  has ' + str(len(d1_only)) + '/' + str(len(data1[ppt])) + ' unique invariants'
        elif data2[ppt]:
            data2_only[ppt] = data2[ppt]
    return (data1_only, data2_only, both)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: ' + os.path.basename(sys.argv[0]) + ' invariantFile1 invariantFile2'
        exit(1)
    if not os.path.isfile(sys.argv[1]):
        print sys.argv[1] + ' is not a file!'
        exit(1)
    if not os.path.isfile(sys.argv[2]):
        print sys.argv[2] + ' is not a file!'
        exit(1)
    inv1 = loadInvariant(sys.argv[1])
    inv2 = loadInvariant(sys.argv[2])
    
    (inv1_only, inv2_only, both) = compareInvs(inv1, inv2)

    for ppt in inv1_only:
        print '=' * 80
        print ppt
        for inv in inv1_only[ppt]:
            print '(1) ' + inv

        if ppt in inv2_only:
            for inv in inv2_only[ppt]:
                print '(2) ' + inv

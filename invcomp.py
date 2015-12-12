#!/usr/bin/env python
# compare two Daikon invariant files (text format)

import os
import sys

def loadInvariant(fileName):
    print 'Loading Invariants from file: ' + fileName
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
                data[ppt] = []
            else:
                data[ppt].append(line.rstrip("\n\r"))
    f.close()
    return data

def printInv(data):
    print 'Invariant file has ' + str(len(data.keys())) + ' Program Points'
    for ppt in data:
        print '=' * 80
        print ppt
        for inv in data[ppt]:
            print '  ' + inv

# data1 is the invariant file for bug-free version 
# data2 is the invariant file for buggy version
# only compare Program Points that exits in both data1 and data2
def compareInv(data1, data2):
    data1_only = {}
    data2_only = {}
    both = {}
    print 'Comparing invariants'
    for ppt in data2:
        if ppt in data1:
            both[ppt] = []
        else:
            data2_only[ppt] = data2[ppt]

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
    printInv(inv1)
    inv2 = loadInvariant(sys.argv[2])
    #print '========================='
    #printInv(inv2)
    
    #diff = compareInv(inv1, inv2)

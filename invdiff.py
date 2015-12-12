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

def compareInv(inv1, inv2):
    print 'Comparing invariants'

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

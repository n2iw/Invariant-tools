#!/usr/bin/env python
# compare two Daikon invariant files (text format)

import os
import sys

def loadInvariantToArrays(fileName):
    #print 'Loading Invariants from file: ' + fileName
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

# ppts is array of all ppt
# invs1 is the invariant arrays for bug-free version 
# data2 is the invariant file for buggy version
# only compare Program Points that exits in both data1 and data2
def compareInvs2(ppts, invs1, data2):
    results = []
    for i in xrange(0, len(ppts)):
        ppt = ppts[i]
        results.append([])
        if ppt in data2:
            for j in xrange(0, len(invs1[i])):
                inv = invs1[i][j]
                if inv in data2[ppt]:
                    results[i].append(0)
                else:
                    results[i].append(1)

        else: #ppt not in buggy version, fill vector with 0s
            for j in xrange(0, len(invs1[i])):
                results[i].append(0)
    return results

def doubleQuotes(s):
    return s.replace('"', '""')

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
    (ppts, invs1) = loadInvariantToArrays(sys.argv[1])
    data2 = loadInvariantToDict(sys.argv[2])
    
    results = compareInvs2(ppts, invs1, data2)

    print '"Program Point","Invariant","' + sys.argv[2] + '"'
    for i in xrange(0, len(ppts)):
        ppt = ppts[i]
        for j in xrange(0, len(invs1[i])):
            print '"' + doubleQuotes(ppt) + '","' + doubleQuotes(invs1[i][j]) + '",' + str(results[i][j])
        

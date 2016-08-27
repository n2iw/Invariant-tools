#!/usr/bin/env python
# compare Daikon invariant files (text format) and count invariant 
# occorence as frequency
# this version is used to compare special buggy invariant files, 
# which contains all the invariants a buggy version violates

import os
import sys
import argparse

def loadInvariantToArrays(f):
    #print 'Loading Invariants from file: ' + fileName
    data = []
    ppts = []
    index = -1
    new_ppt = False
    ppt = None
    lineNum = 0
    while True:
        line = f.readline()
        lineNum += 1
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
                    data[index].append([lineNum, line.rstrip("\n\r")])
    f.close()
    return (ppts, data)

def loadInvariantToDict(f):
    #print 'Loading Invariants from file: ' + fileName
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

# Count invariant occurence
# ppts is array of all ppt
# invs1 is the invariant arrays for bug-free version 
# data2 is the invariant dict for buggy version
#   or if use option -v or --use_violates
#   data2 is the violate dict
# only compare Program Points that exits in both invs1 and data2
# for ppts only in invs1 results will be 0s
def compareInvs2(ppts, invs1, data2):
    for i in xrange(0, len(ppts)):
        ppt = ppts[i]
        if ppt in data2:
            for j in xrange(0, len(invs1[i])):
                if len(invs1[i][j]) < 3:
                    invs1[i][j].append(0)
                inv = invs1[i][j][1]
                if inv in data2[ppt]:
                    invs1[i][j][2] += 1
        else:
            for j in xrange(0, len(invs1[i])):
                if len(invs1[i][j]) < 3:
                    invs1[i][j].append(0)


#replace double quotes " with two double quotes "", required by csv file format
def doubleQuotes(s):
    return s
    # return s.replace('"', '""')

if __name__ == '__main__':
    DLMTR = ','

    parser = argparse.ArgumentParser(description="Compare invariant files and output a matrix in csv format")
    parser.add_argument('fixed', help='(combined)invariant file of fixed version', type=argparse.FileType('r'))
    parser.add_argument('buggy', nargs='+', help='invariant files of buggy versions', type=argparse.FileType('r'))
    parser.add_argument('-n', '--no_names', action='store_true', help="instead of printing program point and invariant names, print line numbers, this option can significantly reduce output file size")
    parser.add_argument('-v', '--use_violates', action='store_true', help="buggy files are violate files instead of invariant files")
    args = parser.parse_args()
    
    (ppts, invs1) = loadInvariantToArrays(args.fixed)

    data = []
    for fileName in args.buggy:
        data.append(loadInvariantToDict(fileName))
        compareInvs2(ppts, invs1, data[-1])

    if args.no_names:
        sys.stdout.write('"Invariant Line Number"')
    else:
        sys.stdout.write('"Program Points"{}"Invariant"'.format(DLMTR))

    sys.stdout.write('{}"{}"'.format(DLMTR ,"Frequency"))
    sys.stdout.write("\n");

    for i in xrange(0, len(ppts)):
        ppt = ppts[i]
        for j in xrange(0, len(invs1[i])):
            if args.no_names:
                sys.stdout.write("{}".format(invs1[i][j][0]))
            else:
                sys.stdout.write('{0}"{1}"{0}"{2}"'.format(DLMTR, doubleQuotes(ppt), doubleQuotes(invs1[i][j][1])))
            sys.stdout.write('{}{}'.format(DLMTR, result[i][j][2]))
            sys.stdout.write("\n")
        

#!/usr/bin/env python
# compare two Daikon invariant files (text format)

import os
import sys

def loadInvariant(fileName):
    #print 'Loading Invariants from file: ' + fileName
    f = open(fileName)
    data = set()
    new_ppt = False
    ignore = False
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
                if not(line.startswith("junit") or line.startswith("daikon")):
                    data.add(line)
    f.close()
    return data

def printInv(data):
    print str(len(data.keys())) + ' Program Points'
    for ppt in data:
        print '=' * 75
        print ppt
        for inv in data[ppt]:
            print '  ' + inv


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: ' + os.path.basename(sys.argv[0]) + ' invariantFile(s)'
        exit(1)
    if not os.path.isfile(sys.argv[1]):
        print sys.argv[1] + ' is not a file!'
        exit(1)

    for f in sys.argv[1:]:
        print f + ' ',
        if not os.path.isfile(f):
            print ''
            print f + ' is not a file!'
            continue
        print 'loading... ',
        data = loadInvariant(f)
        print 'loaded ',
    
        new_file = f + '.ppt'
        of = open(new_file, 'w')
        if not of:
            print ''
            print "Can't write to file: " + f
            continue

        for line in sorted(data):
            of.write(line)

        of.close()
        print 'saved to ' + new_file


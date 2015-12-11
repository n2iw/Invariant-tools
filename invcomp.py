#!/usr/bin/env python
# compare two Daikon invariant files (text format)

import os
import sys

def wav2spx(directory):
    if os.path.isdir(directory):
        files = os.listdir(directory)
        for f in files:
            file = os.path.join(directory, f)
            new_file = file.replace('.wav', '.spx')
            if os.path.isfile(file):
                if file.endswith('.wav'): 
                    print 'convert ' + file + ' to ' + new_file
                    os.system('speexenc --vbr ' + file + ' ' + new_file)
    elif os.path.isfile(directory):
        if directory.endswith('.wav'): # single wav file
            file = directory
            print 'convert ' + file + ' to ' + new_file
            os.system('speexenc --vbr ' + file + ' ' + new_file)
    else:
        print 'Can\'t read file: ' + directory

def loadInvariant(fileName):
    print 'Loading Invariant from file: ' + fileName
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
    print inv1
    inv2 = loadInvariant(sys.argv[2])
    print '========================='
    print inv2
    diff = compareInv(inv1, inv2)

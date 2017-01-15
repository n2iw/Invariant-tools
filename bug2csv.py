#!/usr/bin/env python3
# Extrac bug info from output of "defects4j info -p" command

import os
import sys
import argparse
import re

def loadBugInfo(f):
    print('Loading buginfo from file: ' + str(f.name))
    status = 'start'
    bugs = {}
    while True:
        line = f.readline()
        if line == '': # end of file
            break
        elif line == '\n':
            continue
        elif line.startswith("-----"):
            continue
        elif line.startswith("Summary for Bug:"):
            
            #Start of a new bug
            result = re.search(r'\w+-(\d+)', line)
            bugNum = result.group(1)
            status = 'new'
            print(bugNum)
            continue
        else:
            pass
    f.close()


if __name__ == '__main__':
    DLMTR = ','

    parser = argparse.ArgumentParser(description="Extract bug info into a csv file")
    parser.add_argument('input', help='bug info output from Defects4j', type=argparse.FileType('r'))
    args = parser.parse_args()
    
    loadBugInfo(args.input)

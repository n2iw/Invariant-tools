#!/usr/bin/env python3
# input two invariant matrix (for validation) A and B
# output a matrix only include invariants that are different between A and B

import os
import sys
import argparse
import csv
import re

PPT_COL = 1
START_COL = 3

def getClassMethod(ppt):
    classPattern1 = r"(.*):::(OBJECT|CLASS)$"
    classPattern2 = r"(.*)(\.[^.]+\(.*\)):::(ENTER|EXIT\d*)($|;)"
    result1 = re.match(classPattern1, ppt)
    result2 = re.match(classPattern2, ppt)
    if result1:
        return (result1.group(1), "")
    elif result2:
        return (result2.group(1), result2.group(1) + result2.group(2))
    else:
        print("Can't find class in: {}".format(ppt))
        return ""


def similarity(line1, classes, methods, startCol):
    numSame = 0
    for i in range(startCol, len(line1)):
        if line1[i] == '0':
            continue
        else:
            className, methodName = getClassMethod(line1[PPT_COL])
            if className in classes:
                numSame += 1
                continue
            if methodName in methods:
                numSame += 1
                continue
            line1[i] = '0'
            
    return (numSame)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="compare two matrix (csv) output difference")
    parser.add_argument('first', help='matrix A need to compare', type=argparse.FileType('r'))
    parser.add_argument('second', help='base matrix B', type=argparse.FileType('r'))
    parser.add_argument('-n', '--no-names', action='store_true', help="instead of printing program point and invariant names, print line numbers, this option can significantly reduce output file size")
    parser.add_argument('-q', '--quiet', action='store_true', help="only output statictics")
    args = parser.parse_args()

    reader1 = csv.reader(args.first)
    reader2 = csv.reader(args.second)
    writer = csv.writer(sys.stdout)

    # output header
    header = next(reader1)
    if not args.quiet:
        writer.writerow(header)
    next(reader2)

    # calculate first data column
    startCol = 1
    if not args.no_names:
        startCol = 3

    totalSame = 0

    classes = set()
    methods = set()
    invariants = set()

    for row in reader2:
        className, methodName = getClassMethod(row[PPT_COL])
        for i in range(startCol, len(row)):
            if row[i] == '1':
                classes.add(className)
                methods.add(methodName)
                continue
        

    for line1 in reader1:
        nSame = similarity(line1, classes, methods, startCol)
        totalSame += nSame
        if not args.quiet:
            writer.writerow(line1)

    # print("Total violdations: {}\nTotal filtered: {}\nRemaining violation: {}\nTotal Pass: {}".format(totalViolation, totalFiltered, totalViolation - totalFiltered, totalSame), file=sys.stderr)
    # print("Filter rate: {0:0.2%}%".format(totalFiltered/totalViolation), file=sys.stderr)




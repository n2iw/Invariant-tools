#!/usr/bin/env python3
# input two invariant matrix (for validation) A and B
# output a matrix only include invariants that are different between A and B

import os
import sys
import argparse
import csv


def filter(line1, line2, startCol):
    numViolation = 0
    numFiltered = 0
    numSame = 0
    for i in range(startCol, len(line1)):
        if line1[i] == '0':
            numSame += 1
            continue
        else:
            numViolation += 1
            if line2[i] == '1':
                numFiltered += 1
                line1[i] = '0'
    return (numViolation, numFiltered, numSame)


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

    totalViolation = 0
    totalFiltered = 0
    totalSame = 0

    for line1 in reader1:
        line2 = next(reader2);
        if line1[0] != line2[0]:
            print("{} != {}".format(line1[0], line2[0]))
            sys.exit(1)
        nViolation, nFiltered, nSame = filter(line1, line2, startCol)
        totalViolation += nViolation
        totalFiltered += nFiltered
        totalSame += nSame
        if not args.quiet:
            writer.writerow(line1)

    print("Total violdations: {}\nTotal filtered: {}\nRemaining violation: {}\nTotal Pass: {}".format(totalViolation, totalFiltered, totalViolation - totalFiltered, totalSame), file=sys.stderr)
    print("Filter rate: {0:0.2%}%".format(totalFiltered/totalViolation), file=sys.stderr)




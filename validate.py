#!/usr/bin/env python3
# Validates a set of invariant numbers against a csv file
# output matched lines

import os
import sys
import argparse
import csv

def addRowToSum(sums, row, startCol):
    if len(sums) != len(row):
        print("Array length not equal! Sum's length is {}, Row's length is {}".format(len(sums), len(row) -1))
    for i in range(startCol, len(sums)):
        sums[i] += int(row[i])

def totalDetected(sums, startCol):
    temp = 0
    for s in sums[startCol:]:
        temp += 1 if s > 0 else 0
    return temp


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Validates a set of invariant numbers against a csv file")
    parser.add_argument('csv', help='csv file to Validate', type=argparse.FileType('r'))
    parser.add_argument('invs', nargs='+', help='invariant numbers')
    parser.add_argument('-a', '--adil', action='store_true', help="use csv line number as invariant number" )
    parser.add_argument('-n', '--no-names', action='store_true', help="instead of printing program point and invariant names, print line numbers, this option can significantly reduce output file size")
    args = parser.parse_args()

    invs = set()
    for inv in args.invs:
        invs.add(int(inv))

    reader = csv.reader(args.csv)
    writer = csv.writer(sys.stdout)

    sums = []
    headers = next(reader)
    sums.append('')
    startCol = 1
    if not args.no_names:
        startCol = 3
        sums.append('')
        sums.append('')
    for header in headers[startCol:]:
        sums.append(0)

    writer.writerow(headers)
    lineNum = 0
    for row in reader:
        if args.adil:
            if lineNum in invs:
                addRowToSum(sums, row, startCol)
                writer.writerow(row)
                invs.remove(lineNum)
                if len(invs) == 0:
                    break
        else:
            if int(row[0]) in invs:
                addRowToSum(sums, row, startCol)
                writer.writerow(row)
        lineNum += 1

    sums.append(totalDetected(sums, startCol))
    writer.writerow(sums)

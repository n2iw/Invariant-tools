#!/usr/bin/env python3
# Convert line number Adil use to invariant number in origial csv file (first column)
# first input is original csv file
# rest inputs are Adil-format line numbers
# output array of invairant numbers (sperated by space)
import os
import sys
import argparse
import csv


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Validates a set of invariant numbers against a csv file")
    parser.add_argument('csv', help='csv file to Validate', type=argparse.FileType('r'))
    parser.add_argument('invs', nargs='+', help='invariant numbers')
    parser.add_argument('--headless', action='store_true', help="input csv file doesn't have header line")
    args = parser.parse_args()

    invs = set()
    for inv in args.invs:
        invs.add(int(inv))

    reader = csv.reader(args.csv)
    
    if not args.headless:
        next(reader)

    lineNum = 0
    for row in reader:
        if lineNum in invs:
            print("{} ".format(row[0]), end=" ")
            invs.remove(lineNum)
            if len(invs) == 0:
                break
        lineNum += 1
    print("")

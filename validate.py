#!/usr/bin/env python
# Validates a set of invariant numbers against a csv file
# output matched lines

import os
import sys
import argparse
import csv

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Validates a set of invariant numbers against a csv file")
    parser.add_argument('csv', help='csv file to Validate', type=argparse.FileType('rb'))
    parser.add_argument('invs', nargs='+', help='invariant numbers')
    parser.add_argument('-a', '--adil', action='store_true', help="use csv line number as invariant number" )
    args = parser.parse_args()

    invs = set()
    for inv in args.invs:
        invs.add(int(inv))

    reader = csv.reader(args.csv)
    writer = csv.writer(sys.stdout)

    writer.writerow(reader.next())
    lineNum = 0
    for row in reader:
        if args.adil:
            if lineNum in invs:
                writer.writerow(row)
        else:
            if int(row[0]) in invs:
                writer.writerow(row)
        lineNum += 1

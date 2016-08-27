#!/usr/bin/env python
# Validates a set of invariant numbers against a csv file
# output matched lines

import os
import sys
import argparse
import csv

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Validates a set of invariant numbers against a csv file")
    parser.add_argument('csv', help='csv file to Validate', type=argparse.FileType('r'))
    parser.add_argument('invs', nargs='+', help='invariant numbers')
    args = parser.parse_args()

    invs = set()
    for inv in args.invs:
        invs.add(inv)

    reader = csv.reader(args.csv)
    writer = csv.writer(sys.stdout)

    for row in reader:
        if row[0] in invs:
            writer.writerow(row)

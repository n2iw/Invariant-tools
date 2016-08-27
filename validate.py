#!/usr/bin/env python
# Validates a set of invariant numbers against a csv file
# output matched lines

import os
import sys
import argparse



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Validates a set of invariant numbers against a csv file")
    parser.add_argument('csv', help='csv file to Validate', type=argparse.FileType('r'))
    parser.add_argument('invs', nargs='+', help='invariant numbers')
    args = parser.parse_args()

    invs = set()
    for inv in args.invs:
        invs.add(inv)

    for line in args.csv:
        line = line.rstrip()
        elements = line.split(',')
        if elements[0] in invs:
            print line

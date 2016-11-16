#!/usr/bin/env python
# Filter invariants in a csv file
# only output those without any violations (all 0's)

import os
import sys
import argparse
import csv

def nonFaultSensitive(array):
    for field in array[1:]:
        if field.isdigit() and int(field) != 0: 
            return False
    return True

def faultSensitive(array):
    return not nonFaultSensitive(array)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Filter inviarants in a csv file, only output those without any violations")
    parser.add_argument('csv', help='csv file to Validate', type=argparse.FileType('rb'))

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fault', action='store_true', help='only output fault revealing invariants')
    group.add_argument('--no-fault', action='store_true', help='only output fault revealing invariants')

    args = parser.parse_args()

    reader = csv.reader(args.csv)
    writer = csv.writer(sys.stdout)

    writer.writerow(reader.next())
    for row in reader:
        if args.fault:
            if faultSensitive(row):
                writer.writerow(row)
        elif args.no_fault:
            if nonFaultSensitive(row):
                writer.writerow(row)

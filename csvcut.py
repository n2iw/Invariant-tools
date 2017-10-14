#!/usr/bin/env python3
# Cut a csv file base on columns specified in command line arguments

import os
import sys
import argparse
import csv
import re

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Cut a csv file base on columns specified in command line arguments")
    parser.add_argument('csv', help='csv file to cut', type=argparse.FileType('r'))
    parser.add_argument('startCol', help='start from column')
    parser.add_argument('endCol', help='end at column')
    args = parser.parse_args()

    reader = csv.reader(args.csv)
    writer = csv.writer(sys.stdout)

    startCol = int(args.startCol) - 1
    endCol = int(args.endCol)

    for row in reader:
        writer.writerow(row[startCol:endCol])
        # writer.writerow(row)


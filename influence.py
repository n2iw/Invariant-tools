#!/usr/bin/env python3
# Calculate how many classes and functions a bug affected(influence)
# Input: invariant violation matrix (must have ppt column)
# Output: bug: number_of_affected_classes, number_of_affected_functions 

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
        return ("", "")

def getClass(ppt):
    classPattern1 = r"(.*):::(OBJECT|CLASS)$"
    classPattern2 = r"(.*)\.[^.]+\(.*\):::(ENTER|EXIT\d*)($|;)"
    result1 = re.match(classPattern1, ppt)
    result2 = re.match(classPattern2, ppt)
    if result1:
        return result1.group(1)
    elif result2:
        return result2.group(1)
    else:
        print("Can't find class in: {}".format(ppt))
        return ""

    return ppt

def getMethod(ppt):
    methodPattern = r"(.*):::(ENTER|EXIT\d*)($|;)"
    result = re.match(methodPattern, ppt)
    if result:
        return result.group(1)
    else:
        # print("Can't find method in: {}".format(ppt))
        return ""


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Calculate how many classes and functions a bug affected(influence)")
    parser.add_argument('csv', help='csv file to Caculate', type=argparse.FileType('r'))
    parser.add_argument('-v', '--verbose', action='store_true', help="output affected classes and function names")
    args = parser.parse_args()
    csv.field_size_limit(sys.maxsize)

    reader = csv.reader(args.csv)
    writer = csv.writer(sys.stdout)

    headers = next(reader)
    bugs = {}
    classes = {}
    methods = {}
    invariants = {}
    for i in range(START_COL, len(headers)):
        invariants[i] = 0
        bugs[i] = headers[i]
        classes[i] = set()
        methods[i] = set()

    lineNum = 0
    all_classes = set()
    affected_classes = set()
    all_methods = set()
    affected_methods = set()
    for row in reader:
        # className = getClass(row[PPT_COL])
        # methodName = getMethod(row[PPT_COL])
        className, methodName = getClassMethod(row[PPT_COL])
        if className:
            all_classes.add(className)
        if methodName:
            all_methods.add(methodName)
        for i in range(START_COL, len(headers)):
            if row[i] == '1':
                invariants[i] += 1
                classes[i].add(className)
                affected_classes.add(className)
                if len(methodName) != 0:
                    methods[i].add(methodName)
                    affected_methods.add(methodName)
        lineNum += 1

    for i in range(START_COL, len(headers)):
        print("=" * 75)
        print("{}: {}".format(i, bugs[i]))
        print("Classes: {}".format(len(classes[i])))
        if args.verbose:
            for c in classes[i]:
                print(c)
        print("Methods: {}".format(len(methods[i])))
        if args.verbose:
            for m in methods[i]:
                print(m)
        print("Invariants: {}".format(invariants[i]))

    print("Total invariants: {}".format(lineNum))
    print("Total classes: {}".format(len(all_classes)))
    print("Affected classes: {}".format(len(affected_classes)))
    print("Total methods: {}".format(len(all_methods)))
    print("Affected methods: {}".format(len(affected_methods)))

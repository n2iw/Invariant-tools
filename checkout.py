#!/usr/bin/python

import sys, os
import argparse

FIRST_NUM = 1
LAST_NUM = 133
PREFIX = os.environ['PWD'] + '/'
PROJECT = 'Closure'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Checkout programs of Closure")

    # run in folder
    parser.add_argument('--prefix', help="parent folder of all fixed and buggy folders" ,
            default=PREFIX)

    # run buggy of fixed version
    kind_group = parser.add_mutually_exclusive_group(required=True)
    kind_group.add_argument('-f', '--fixed', help='Run fixed versions', action='store_true')
    kind_group.add_argument('-b', '--buggy', help='Run buggy versions', action='store_true')
    # version range
    parser.add_argument('first', type=int, help='first version')
    parser.add_argument('last', type=int, help='last version')
    parser.add_argument('-d', '--dry-run', help="only print commands, won't run it" , action='store_true')

    args = parser.parse_args()

    if args.first < FIRST_NUM:
        print "First bug number must be greater than or equal to {}".format(FIRST_NUM) 
        exit(1)

    if args.last > LAST_NUM:
        print "Last bug number must be less than or equal to {}".format(LAST_NUM)
        exit(1)


    for i in xrange(args.first, args.last + 1):
        if args.fixed:
            kind = 'fix'
            version = 'f'
        else:
            kind = 'buggy'
            version = 'b'
        folder = "{}_{}".format(kind, str(i))
        cmd = "defects4j checkout -p {} ".format(PROJECT)
        cmd += "-v {}{} ".format(i, version) 
        cmd += "-w " + folder
        print cmd
        if not args.dry_run:
            os.system(cmd)

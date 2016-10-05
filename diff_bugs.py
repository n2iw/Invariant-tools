#!/usr/bin/python

import sys, os

if len(sys.argv) != 3:
    print "Usage: " + sys.argv[0] + " firstNumber lastNumber"
    exit(1)

for i in xrange(int(sys.argv[1]), int(sys.argv[2]) + 1):
    fix_folder = "fix_" + str(i)
    buggy_folder = "buggy_" + str(i)
    diff_file = "results/diff/buggy_" + str(i) + '.diff'
    cmd = "diff -r " 
    cmd += buggy_folder + "/src/main/java/ "
    cmd += fix_folder + "/src/main/java/ " 
    cmd += "> " + diff_file
    print cmd
    os.system(cmd)

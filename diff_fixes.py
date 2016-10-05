#!/usr/bin/python

import sys, os

if len(sys.argv) != 4:
    print "Usage: " + sys.argv[0] + " baseNumber firstNumber lastNumber"
    exit(1)

base = sys.argv[1]
base_version = "fix_" + str(base)
diff_dir = "diff/fix_" + str(base)
cmd = "mkdir -p " + diff_dir
print cmd
os.system(cmd)
for i in xrange(int(sys.argv[2]), int(sys.argv[3]) + 1):
    compare_version = "fix_" + str(i)
    diff_file = diff_dir + "/" + str(base) + '_' + str(i) + '.diff'
    cmd = "diff -r " 
    cmd += compare_version + "/src/main/java/ "
    cmd += base_version + "/src/main/java/ " 
    cmd += "> " + diff_file
    print cmd
    os.system(cmd)

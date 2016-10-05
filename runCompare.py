#!/usr/bin/python

from run_lib import *

import os, sys
import datetime

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: " + sys.argv[0] + " first_bug_number last_bug_number(<=35)"
        exit(1)
    first = int(sys.argv[1])
    last = int(sys.argv[2])

    if first < 1:
        print "First bug number must be greater than or equal to 1"
        exit(1)

    if last > 27:
        print "Last bug number must be less than or equal to 27"
        exit(1)

    folder = 'results'
    run_in_folder(folder, ['mkdir -p violates'], False)

    for i in xrange(first, last + 1):
        print '=' * 75
        print 'version ' + str(i)
        #if i not in versions:
            #print 'buggy_' + str(i) + ' skipped!'
            #continue

        cmds = []

        cmd = 'invViolates.py '
        cmd += 'fixed/fix_{0}.txt '.format(i)
        cmd += 'buggy/buggy_{0}.txt '.format(i) 
        cmd += '> violates/buggy_{0}.txt '.format(i)   
        cmds.append(cmd)

        run_in_folder(folder, cmds, False)



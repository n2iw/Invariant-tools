#!/usr/bin/python

import argparse
import os
import sys
import subprocess
import re


FIRST_NUM = 1
LAST_NUM = 133 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find programs that needs to be run")

    #  buggy of fixed version
    kind_group = parser.add_mutually_exclusive_group(required=True)
    kind_group.add_argument('-f', '--fixed', help='Check fixed versions', action='store_true')
    kind_group.add_argument('-b', '--buggy', help='Check buggy versions', action='store_true')
    # version range
    parser.add_argument('first', type=int, help='first version')
    parser.add_argument('last', type=int, help='last version')
    parser.add_argument('-v', '--verbose', help='Print status for every program', action='store_true', default=False)

    args = parser.parse_args()

    if args.first < FIRST_NUM:
        print "First bug number must be greater than or equal to {}".format(FIRST_NUM) 
        exit(1)

    if args.last > LAST_NUM:
        print "Last bug number must be less than or equal to {}".format(LAST_NUM)
        exit(1)


    if args.fixed:
        kind = 'fix'
    elif args.buggy:
        kind = 'buggy'


    for i in range(args.first, args.last + 1):
        status_cmd = [ "submit", "--status" ]

        version = '{}_{}'.format(kind, i)

        if os.path.isfile("results/{}.txt".format(version)):
            if args.verbose:
                print("{} is done".format(version))
            continue
        elif os.path.isfile("{}.txt".format(version)):
            if args.verbose:
                print("{} has finished, need to be confirmed".format(version))
            continue


        grep_cmd = 'grep -l {}.py 0000*/*/*.sh'.format(version)

        try: 
            out = subprocess.check_output(grep_cmd, shell=True)
            jobID = out[:8]

            if args.verbose:
                status_cmd.append(jobID)
                # print(status_cmd)
                try: 
                    job = subprocess.Popen(status_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, error = job.communicate()
                    result = re.search(r'(Running|Pending)', out, re.IGNORECASE & re.MULTILINE)
                    status = result.group(0)
                    print("{} is {} on cluster".format(version, status))
                except  OSError as e:
                    print("{} has been submitted to cluster, status unknown".format(version))
                    pass
        except  subprocess.CalledProcessError as e:
            print i


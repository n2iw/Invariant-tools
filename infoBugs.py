#!/usr/bin/env python3

import os
import argparse

def info_bugs(project, num):
    for i in range(1, num + 1):
        cmd = 'defects4j info -p {0} -b {1} >> {0}_bugs.txt'.format(project, i)
        print(cmd)
        os.system(cmd)



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Get bug infomation for Defect4j project")
    parser.add_argument('project', help='Project name')
    parser.add_argument('max', type=int, help='Max bug number')
    args = parser.parse_args()

    info_bugs(args.project, args.max)

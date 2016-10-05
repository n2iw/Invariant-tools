#!/usr/bin/python

import datetime
import argparse
import os
import sys


FIRST_NUM = 1
LAST_NUM = 60 
JUNIT = '$PWD/lib/junit-3.8.2.jar'
# SAMPLE = ' --sample-start=100'
SAMPLE = ' '
OPTIONS_TMP = " --noversion --omit_from_output 0r --no_text_output -o {}"
TEST_CLASS = ' daikonTest'
PACKAGE = 'org.joda.time'
ARGS = 'echo'
for a in sys.argv:
    ARGS += ' ' + a
LOAD_JAVA = 'module load java/1.7.0_25'
HOST_NAME = 'hostname'
LSCPU = 'lscpu | grep "^CPU(s)"'
FREE = 'free -h'
COMPARABILITY_FILES = ['org.joda.time.TestAll.decls-DynComp' , 
        'org.joda.time.chrono.TestAll.decls-DynComp' ,
        'org.joda.time.chrono.gj.TestAll.decls-DynComp' ,
        'org.joda.time.convert.TestAll.decls-DynComp' ,
        'org.joda.time.field.TestAll.decls-DynComp' ,
        'org.joda.time.format.TestAll.decls-DynComp' ,
        'org.joda.time.tz.TestAll.decls-DynComp'
        ]
# omit_ppt_options = ' --ppt-omit-pattern=Test '
omit_ppt_options = ' '

def generate_script(version, cmds, dry_run):
    fileName = "{}.sh".format(version)
    if not dry_run:
        of = open(fileName, 'w')
        of.write("#!/bin/sh\n")
        for cmd in cmds:
            of.write(cmd + "\n")
        of.close()
        os.chmod(fileName, 0755)
    else:
        for cmd in cmds:
            print(cmd)

def submit(version, queue, ncpus, wall_time, dry_run):
    cmd = "submit --detach -v {0} -M -n{1} -N{1} -w{2}  -i ./{3}/ -i ./lib/  ./{3}.sh".format(queue, ncpus, wall_time, version)
    print(cmd)
    if not dry_run:
        os.system(cmd)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run tasks on Time project")

    # run buggy of fixed version
    kind_group = parser.add_mutually_exclusive_group(required=True)
    kind_group.add_argument('-f', '--fixed', help='Run fixed versions', action='store_true')
    kind_group.add_argument('-b', '--buggy', help='Run buggy versions', action='store_true')
    # version range
    parser.add_argument('first', type=int, help='first version')
    parser.add_argument('last', type=int, help='last version')
    # commands to run
    parser.add_argument('task', help='task to run', choices=['runDaikon', 'runDaikonOnline'])
    parser.add_argument('-m', '--target-mem', type=int, help='memory size', default=2)
    parser.add_argument('-M', '--daikon-mem', type=int, help='memory size', default=8)
    parser.add_argument('-d', '--dry-run', help="only print commands, won't run it" , action='store_true')
    parser.add_argument('-v', '--queue', help='Cluster queue to use', default='u2-grid')
    parser.add_argument('-n', '--ncpus', type=int, help='cpus to require', default=8)
    parser.add_argument('-w', '--wall-time', type=int, help='wall time', default=480)

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
    else:
        kind = 'buggy'
        print 'Should provide --buggy or --fixed'

    CONVERT = '$PWD/lib/joda-convert-1.2.jar'
    DAIKON = '$PWD/lib/daikon.jar' 
    COMPARABILITY = ''
    for c in COMPARABILITY_FILES:
        COMPARABILITY += ' --comparability-file=$PWD/lib/{}'.format(c)
    select_ppt_option = " --ppt-select-pattern={}".format(PACKAGE)

    for i in range(args.first, args.last + 1):
        print '=' * 75
        print 'version ' + str(i)

        version = '{}_{}'.format(kind, i)
        CP = '$PWD/{}/target/test-classes:'.format(version)
        CP += '$PWD/{}/target/classes '.format(version)
        dtraceFile = '{}_{}.dtrace.gz'.format(kind, i)
        dtraceOutput = ' --dtrace-file=' + dtraceFile
        invFile = '{}_{}.inv.gz'.format(kind, i)
        OPTIONS = OPTIONS_TMP.format(invFile)

        cmds = []

        cmds.append(ARGS)
        cmds.append(LOAD_JAVA)
        cmds.append(HOST_NAME)
        cmds.append(LSCPU)
        cmds.append(FREE)
        cmd = 'java -d64 -Xmx{}g -cp'.format(args.target_mem)
        cmd += ' {}:{}:{}:'.format(DAIKON, JUNIT, CONVERT)
        cmd += CP
        cmd += ' daikon.Chicory '
        cmd += select_ppt_option  
        cmd += omit_ppt_options
        cmd += SAMPLE
        cmd += COMPARABILITY
        cmd += ' --heap-size={}g'.format(args.daikon_mem)
        cmd += ' --daikon-args="{}"'.format(OPTIONS)
        if args.task == 'runDaikon':
            # do run daikon on cluster
            cmd += dtraceOutput
            cmd += ' --daikon'
            cmd += TEST_CLASS
            cmds.append(cmd)

        elif args.task == 'runDaikonOnline':
            #do run daikon online on cluster no intermedia dtrace file will be generated
            cmd += ' --daikon-online'
            cmd += TEST_CLASS
            cmds.append(cmd)
        else:
            print "invalid command: " + task
            exit(1)

        generate_script(version, cmds, args.dry_run)
        submit(version, args.queue, args.ncpus, args.wall_time, args.dry_run)

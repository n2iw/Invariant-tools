#!/usr/bin/python

import datetime
import argparse
import os

from run_lib import *

FIRST_NUM = 1
LAST_NUM = 27 
PREFIX = os.environ['PWD'] + '/'
#SAMPLE = ' --sample-start=100'
SAMPLE = ' '
COMPARABILITY = ' '
OPTIONS_TMP = " -o {}"
TEST_CLASS = ' MainTest'
TEST_FILE = 'Main.java'
MEM = '8'

omit_ppt_options = ' '
select_ppt_option = ' '



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run tasks on Lang project")

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
    # commands to run
    parser.add_argument('tasks', nargs='+', help='task to run', 
            choices=['copy', 'compile', 'run','runFrontend', 'runDaikonInline', 'runDaikon', 'runDaikonOnline', 'print', 'clean'])
    parser.add_argument('-d', '--dry-run', help="only print commands, won't run it" , action='store_true')
    parser.add_argument('-m', '--memory', help="maximum memory usage in GB" , type=int, default=MEM)

    args = parser.parse_args()

    if args.first < FIRST_NUM:
        print "First bug number must be greater than or equal to {}".format(FIRST_NUM) 
        exit(1)

    if args.last > LAST_NUM:
        print "Last bug number must be less than or equal to {}".format(LAST_NUM)
        exit(1)

    versions = xrange(FIRST_NUM, LAST_NUM + 1)

    if args.fixed:
        kind = 'fix'
    elif args.buggy:
        kind = 'buggy'

    DAIKON = args.prefix + 'lib/daikon.jar' 
    JUNIT = args.prefix + 'lib/junit-4.11.jar'

    for i in xrange(args.first, args.last + 1):
        print '=' * 75
        print 'version ' + str(i)
        if i not in versions:
            print '{}_{} skipped!'.format(kind, i)
            continue

        folder = '{}_{}'.format(kind, i)
        CP = args.prefix + folder + '/target/test-classes:'
        CP += args.prefix + folder + '/target/classes '

        cmds = []

        for task in args.tasks:

            if task == 'compile':
                #compile
                cmds.append('mvn test-compile')
            elif task == 'copy':
                cmd = 'cp ../{} src/test/java/'.format(TEST_FILE)
                cmds.append(cmd)
            elif task == 'run':
                #run directly
                cmd = 'java -d64 -Xmx{}g -cp'.format(args.memory)
                cmd += ' {}:'.format(JUNIT)
                cmd += CP
                cmd += TEST_CLASS
                cmds.append(cmd)
            elif task == 'runFrontend':
                #do run daikon front end on it
                dtraceFile = '{}_{}.dtrace.gz'.format(kind, i)
                dtraceOutput = ' --dtrace-file=' + dtraceFile

                cmd = 'java -d64 -Xmx{}g -cp'.format(args.memory)
                cmd += ' {}:{}:'.format(DAIKON, JUNIT)
                cmd += CP
                cmd += ' daikon.Chicory '
                cmd += select_ppt_option  
                cmd += omit_ppt_options
                cmd += SAMPLE
                cmd += COMPARABILITY
                cmd += dtraceOutput
                cmd += TEST_CLASS
                cmds.append(cmd)
            elif task == 'runDaikonInline':
                #do run daikon frontend and daikon all at once
                dtraceFile = '{}_{}.dtrace.gz'.format(kind, i)
                dtraceOutput = ' --dtrace-file=' + dtraceFile

                cmd = 'java -d64 -Xmx{}g -cp'.format(args.memory)
                cmd += ' {}:{}:'.format(DAIKON, JUNIT)
                cmd += CP
                cmd += ' daikon.Chicory --daikon '
                cmd += select_ppt_option  
                cmd += omit_ppt_options
                cmd += SAMPLE
                cmd += COMPARABILITY
                cmd += dtraceOutput
                cmd += TEST_CLASS
                cmds.append(cmd)
            elif task == 'runDaikon':
                #run daikon on it

                dtraceFile = '{}_{}.dtrace.gz'.format(kind, i)
                invFile = '{}_{}.inv.gz'.format(kind, i)
                OPTIONS = OPTIONS_TMP.format(invFile)

                cmd = 'java -d64 -Xmx{}g -cp'.format(args.memory)
                cmd += ' ' + DAIKON
                cmd += ' daikon.Daikon'
                cmd += OPTIONS
                cmd += ' ' + dtraceFile
                cmds.append(cmd)
            elif task == 'runDaikonOnline':
                #do run daikon online no intermedia dtrace file will be generated

                invFile = '{}_{}.inv.gz'.format(kind, i)
                OPTIONS = OPTIONS_TMP.format(invFile)

                cmd = 'java -d64 -Xmx{}g -cp'.format(args.memory)
                cmd += ' {}:{}:'.format(DAIKON, JUNIT)
                cmd += CP
                cmd += ' daikon.Chicory'
                cmd += select_ppt_option
                cmd += omit_ppt_options
                cmd += SAMPLE
                cmd += ' --daikon-online'
                cmd += ' --heap-size={}g'.format(args.memory - 1)
                cmd += ' --daikon-args="{}"'.format(OPTIONS)
                cmd += TEST_CLASS
                cmds.append(cmd)
            elif task == 'print':
                # print invaraints
                invFile = '{}_{}.inv.gz'.format(kind, i)

                cmd = 'java -d64 -Xmx{}g -cp '.format(args.memory)
                cmd += DAIKON
                cmd += ' daikon.PrintInvariants '
                cmd += invFile
                cmd += ' > ../{}_{}.txt'.format(kind, i)
                cmds.append(cmd)
            elif task == 'clean':
                # remove all dtrace files if corresponding inv files exist
                dtraceFile = '{}_{}.dtrace.gz'.format(kind, i)
                invFile = '{}_{}.inv.gz'.format(kind, i)
                #print 'dtraceFile="{}"'.format(dtraceFile)
                #print 'invFile="{}"'.format(invFile)
            
                if os.path.exists("{}/{}".format(folder, dtraceFile)) and os.path.exists("{}/{}".format(folder, invFile)):
                    cmd = 'rm ' + dtraceFile
                    cmds.append(cmd)
            else:
                print "invalid command: " + task
                exit(1)

        run_in_folder(folder, cmds, args.dry_run)


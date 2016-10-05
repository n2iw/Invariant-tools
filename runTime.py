#!/usr/bin/python

import datetime
import argparse
import os

from run_lib import *

FIRST_NUM = 1
LAST_NUM = 60 
PREFIX = os.environ['PWD'] + '/'
JUNIT = PREFIX + 'lib/junit-3.8.2.jar'
SAMPLE = ' --sample-start=100'
OPTIONS_TMP = " --noversion --omit_from_output 0r --no_text_output -o {}"
TEST_CLASS = ' daikonTest'
TEST_FILE = 'daikonTest.java'
PACKAGES = [
        'org.joda.time',
        'org.joda.time.base',
        'org.joda.time.chrono',
        'org.joda.time.convert',
        'org.joda.time.field',
        'org.joda.time.format',
        'org.joda.time.tz',
        'org.joda.time.DateTimeZone.forOffsetHoursMinutes'

        ]

COMPARABILITY_FILES = ['org.joda.time.TestAll.decls-DynComp' , 
        'org.joda.time.chrono.TestAll.decls-DynComp' ,
        'org.joda.time.chrono.gj.TestAll.decls-DynComp' ,
        'org.joda.time.convert.TestAll.decls-DynComp' ,
        'org.joda.time.field.TestAll.decls-DynComp' ,
        'org.joda.time.format.TestAll.decls-DynComp' ,
        'org.joda.time.tz.TestAll.decls-DynComp'
        ]

omit_ppt_options = ' --ppt-omit-pattern=Test '



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run tasks on Time project")

    # restric and ppt files
    parser.add_argument('-r', '--restrict-file', help='only run versions in restrict file', type=argparse.FileType('r'))
    parser.add_argument('-p', '--ppt-file', help='all ppts that will be used to part the program running', type=argparse.FileType('r'))
    # run in folder
    parser.add_argument('--prefix', help="parent folder of all fixed and buggy folders" ,
            default=PREFIX)
    #select and exlude ppts
    ppt_group = parser.add_mutually_exclusive_group(required=True)
    ppt_group.add_argument('-s', '--select-ppt', type=int, help='select which ppt(index) to process and output')
    ppt_group.add_argument('-se', '--each-ppts', action='store_true', help='run for each ppts one by one')
    ppt_group.add_argument('-sa', '--all-ppts', action='store_true', help='run for all ppts together')
    parser.add_argument('-x', '--exclude-ppts', type=int, action='append', help='run for all ppts one by one')
    # run buggy of fixed version
    kind_group = parser.add_mutually_exclusive_group(required=True)
    kind_group.add_argument('-f', '--fixed', help='Run fixed versions', action='store_true')
    kind_group.add_argument('-b', '--buggy', help='Run buggy versions', action='store_true')
    # version range
    parser.add_argument('first', type=int, help='first version')
    parser.add_argument('last', type=int, help='last version')
    # commands to run
    parser.add_argument('tasks', nargs='+', help='task to run', 
            choices=['copy', 'compile', 'run', 'runFrontend', 'runDaikon', 'runDaikonOnline', 'print', 'clean'])
    parser.add_argument('-d', '--dry-run', help="only print commands, won't run it" , action='store_true')

    args = parser.parse_args()

    if args.first < FIRST_NUM:
        print "First bug number must be greater than or equal to {}".format(FIRST_NUM) 
        exit(1)

    if args.last > LAST_NUM:
        print "Last bug number must be less than or equal to {}".format(LAST_NUM)
        exit(1)

    if args.restrict_file:
        versions = loadRestricts(args.restrict_file)
    else:
        versions = xrange(FIRST_NUM, LAST_NUM + 1)

    if args.ppt_file:
        PACKAGES = loadPPTs(args.ppt_file)

    if args.each_ppts:
        ppt_filter = set()
        if args.exclude_ppts:
            ppt_filter = set(args.exclude_ppts)
        ppts = set(xrange(0, len(PACKAGES))) - set(ppt_filter) 
    elif args.all_ppts:
        ppts = [0] 
    elif args.select_ppt >= len(PACKAGES) or args.select_ppt < 0:
        print 'selected ppt out of range [{}, {}]'.format(0, len(PACKAGES) -1)
        exit(1)
    else:
        ppts = [args.select_ppt]

    if args.fixed:
        kind = 'fix'
    elif args.buggy:
        kind = 'buggy'
    else:
        kind = 'buggy'
        print 'Should provide --buggy or --fixed'

    CONVERT = args.prefix + 'lib/joda-convert-1.2.jar'
    DAIKON = args.prefix + 'lib/daikon.jar' 

    COMPARABILITY = ''
    for c in COMPARABILITY_FILES:
        COMPARABILITY += ' --comparability-file={}lib/{}'.format(args.prefix, c)

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
                cmd = 'java -d64 -Xmx8g -cp'
                cmd += ' {}:{}:'.format(JUNIT, CONVERT)
                cmd += CP
                cmd += TEST_CLASS
                cmds.append(cmd)
            elif task == 'runFrontend':
                #do run daikon front end on it
                for j in ppts:
                    ppt = PACKAGES[j]
                    select_ppt_option = " --ppt-select-pattern={}".format(ppt)
                    if j == 0 and args.each_ppts:
                        for p in PACKAGES[1:]:
                            omit_ppt_options += " --ppt-omit-pattern={}".format(p)

                    dtraceFile = '{}_{}_{}.dtrace.gz'.format(kind, i, ppt)
                    dtraceOutput = ' --dtrace-file=' + dtraceFile

                    cmd = 'java -d64 -Xmx8g -cp'
                    cmd += ' {}:{}:{}:'.format(DAIKON, JUNIT, CONVERT)
                    cmd += CP
                    cmd += ' daikon.Chicory '
                    cmd += select_ppt_option  
                    cmd += omit_ppt_options
                    cmd += SAMPLE
                    cmd += COMPARABILITY
                    cmd += dtraceOutput
                    cmd += TEST_CLASS
                    cmds.append(cmd)
            elif task == 'runDaikon':
                #run daikon on it
                for j in ppts:
                    ppt = PACKAGES[j]
                    select_ppt_option = " --ppt-select-pattern={}".format(ppt)
                    if j == 0 and args.each_ppts:
                        for p in PACKAGES[1:]:
                            omit_ppt_options += " --ppt-omit-pattern={}".format(p)

                    dtraceFile = '{}_{}_{}.dtrace.gz'.format(kind, i, ppt)
                    invFile = '{}_{}_{}.inv.gz'.format(kind, i, ppt)
                    OPTIONS = OPTIONS_TMP.format(invFile)

                    cmd = 'java -d64 -Xmx8g -cp'
                    cmd += ' ' + DAIKON
                    cmd += ' daikon.Daikon'
                    cmd += OPTIONS
                    cmd += ' ' + dtraceFile
                    cmds.append(cmd)
            elif task == 'runDaikonOnline':
                #do run daikon online no intermedia dtrace file will be generated
                for j in ppts:
                    ppt = PACKAGES[j]
                    select_ppt_option = " --ppt-select-pattern={}".format(ppt)
                    if j == 0 and args.each_ppts:
                        for p in PACKAGES[1:]:
                            omit_ppt_options += " --ppt-omit-pattern={}".format(p)

                    invFile = '{}_{}_{}.inv.gz'.format(kind, i, ppt)
                    OPTIONS = OPTIONS_TMP.format(invFile)

                    cmd = 'java -d64 -Xmx8g -cp'
                    cmd += ' {}:{}:{}:'.format(DAIKON, JUNIT, CONVERT)
                    cmd += CP
                    cmd += ' daikon.Chicory'
                    cmd += select_ppt_option
                    cmd += omit_ppt_options
                    cmd += SAMPLE
                    cmd += ' --daikon-online'
                    cmd += ' --heap-size=7g'
                    cmd += ' --daikon-args="{}"'.format(OPTIONS)
                    cmd += TEST_CLASS
                    cmds.append(cmd)
            elif task == 'print':
                # print invaraints
                for j in ppts:
                    ppt = PACKAGES[j]
                    invFile = '{}_{}_{}.inv.gz'.format(kind, i, ppt)

                    cmd = 'java -d64 -Xmx8g -cp '
                    cmd += DAIKON
                    cmd += ' daikon.PrintInvariants '
                    cmd += invFile
                    cmd += ' > ../{}_{}_{}.txt'.format(kind, i, ppt)
                    cmds.append(cmd)
            elif task == 'clean':
                # remove all dtrace files if corresponding inv files exist
                for j in ppts:
                    ppt = PACKAGES[j]
                    dtraceFile = '{}_{}_{}.dtrace.gz'.format(kind, i, ppt)
                    invFile = '{}_{}_{}.inv.gz'.format(kind, i, ppt)
                    #print 'dtraceFile="{}"'.format(dtraceFile)
                    #print 'invFile="{}"'.format(invFile)
                
                    if os.path.exists("{}/{}".format(folder, dtraceFile)) and os.path.exists("{}/{}".format(folder, invFile)):
                        cmd = 'rm ' + dtraceFile
                        cmds.append(cmd)
            else:
                print "invalid command: " + task
                exit(1)

        run_in_folder(folder, cmds, args.dry_run)

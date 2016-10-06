#!/usr/bin/python

import argparse
import os
import sys
import subprocess


FIRST_NUM = 1
LAST_NUM = 15 
JUNIT = '$PWD/lib/junit-4.11.jar'
# SAMPLE = ' --sample-start=100'
SAMPLE = ' '
OPTIONS_TMP = ' --noversion --omit_from_output 0r --no_text_output --config_option daikon.FileIO.count_lines=false -o {}'
TEST_CLASS = ' MainTest'
PACKAGE = 'org.apache.commons.lang3'
ARGS = 'echo'
for a in sys.argv:
    ARGS += ' ' + a
LOAD_JAVA = 'module load java/1.7.0_25'
HOST_NAME = 'hostname'
LSCPU = 'lscpu | grep "^CPU(s)"'
FREE = 'free -h'
select_ppt_template = ' --ppt-select-pattern="{}"'
omit_ppt_template = ' --ppt-omit-pattern="{}"'
omit_ppt_options = ' '

CHICORY_MEM = '3'
TARGET_MEM = '8'
DAIKON_MEM = '8'
QUEUE = 'u2-grid'
NCPUS =  8
WALL_TIME =  72 * 60
COMPARABILITY = ''
# VISIBILITY = ' --std-visibility'
VISIBILITY = ' '

PACKAGES = [
        'org.apache.commons.lang3',
        'org.apache.commons.lang3.builder',
        'org.apache.commons.lang3.concurrent',
        'org.apache.commons.lang3.event',
        'org.apache.commons.lang3.exception',
        'org.apache.commons.lang3.math',
        'org.apache.commons.lang3.mutable',
        'org.apache.commons.lang3.reflect',
        'org.apache.commons.lang3.text',
        'org.apache.commons.lang3.text.translate',
        'org.apache.commons.lang3.time',
        'org.apache.commons.lang3.tuple'
        ]

CLASSES = [
        'org.apache.commons.lang3.AnnotationUtils.java',
        'org.apache.commons.lang3.ArrayUtils.java',
        'org.apache.commons.lang3.BitField.java',
        'org.apache.commons.lang3.BooleanUtils.java',
        'org.apache.commons.lang3.builder.Builder.java',
        'org.apache.commons.lang3.builder.CompareToBuilder.java',
        'org.apache.commons.lang3.builder.EqualsBuilder.java',
        'org.apache.commons.lang3.builder.HashCodeBuilder.java',
        'org.apache.commons.lang3.builder.IDKey.java',
        'org.apache.commons.lang3.builder.ReflectionToStringBuilder.java',
        'org.apache.commons.lang3.builder.StandardToStringStyle.java',
        'org.apache.commons.lang3.builder.ToStringBuilder.java',
        'org.apache.commons.lang3.builder.ToStringStyle.java',
        'org.apache.commons.lang3.CharEncoding.java',
        'org.apache.commons.lang3.CharRange.java',
        'org.apache.commons.lang3.CharSequenceUtils.java',
        'org.apache.commons.lang3.CharSet.java',
        'org.apache.commons.lang3.CharSetUtils.java',
        'org.apache.commons.lang3.CharUtils.java',
        'org.apache.commons.lang3.ClassUtils.java',
        'org.apache.commons.lang3.concurrent.AtomicInitializer.java',
        'org.apache.commons.lang3.concurrent.AtomicSafeInitializer.java',
        'org.apache.commons.lang3.concurrent.BackgroundInitializer.java',
        'org.apache.commons.lang3.concurrent.BasicThreadFactory.java',
        'org.apache.commons.lang3.concurrent.CallableBackgroundInitializer.java',
        'org.apache.commons.lang3.concurrent.ConcurrentException.java',
        'org.apache.commons.lang3.concurrent.ConcurrentInitializer.java',
        'org.apache.commons.lang3.concurrent.ConcurrentRuntimeException.java',
        'org.apache.commons.lang3.concurrent.ConcurrentUtils.java',
        'org.apache.commons.lang3.concurrent.ConstantInitializer.java',
        'org.apache.commons.lang3.concurrent.LazyInitializer.java',
        'org.apache.commons.lang3.concurrent.MultiBackgroundInitializer.java',
        'org.apache.commons.lang3.concurrent.TimedSemaphore.java',
        'org.apache.commons.lang3.Conversion.java',
        'org.apache.commons.lang3.EnumUtils.java',
        'org.apache.commons.lang3.event.EventListenerSupport.java',
        'org.apache.commons.lang3.event.EventUtils.java',
        'org.apache.commons.lang3.exception.CloneFailedException.java',
        'org.apache.commons.lang3.exception.ContextedException.java',
        'org.apache.commons.lang3.exception.ContextedRuntimeException.java',
        'org.apache.commons.lang3.exception.DefaultExceptionContext.java',
        'org.apache.commons.lang3.exception.ExceptionContext.java',
        'org.apache.commons.lang3.exception.ExceptionUtils.java',
        'org.apache.commons.lang3.JavaVersion.java',
        'org.apache.commons.lang3.LocaleUtils.java',
        'org.apache.commons.lang3.math.Fraction.java',
        'org.apache.commons.lang3.math.IEEE754rUtils.java',
        'org.apache.commons.lang3.math.NumberUtils.java',
        'org.apache.commons.lang3.mutable.Mutable.java',
        'org.apache.commons.lang3.mutable.MutableBoolean.java',
        'org.apache.commons.lang3.mutable.MutableByte.java',
        'org.apache.commons.lang3.mutable.MutableDouble.java',
        'org.apache.commons.lang3.mutable.MutableFloat.java',
        'org.apache.commons.lang3.mutable.MutableInt.java',
        'org.apache.commons.lang3.mutable.MutableLong.java',
        'org.apache.commons.lang3.mutable.MutableObject.java',
        'org.apache.commons.lang3.mutable.MutableShort.java',
        'org.apache.commons.lang3.ObjectUtils.java',
        'org.apache.commons.lang3.RandomStringUtils.java',
        'org.apache.commons.lang3.Range.java',
        'org.apache.commons.lang3.reflect.ConstructorUtils.java',
        'org.apache.commons.lang3.reflect.FieldUtils.java',
        'org.apache.commons.lang3.reflect.MemberUtils.java',
        'org.apache.commons.lang3.reflect.MethodUtils.java',
        'org.apache.commons.lang3.reflect.TypeUtils.java',
        'org.apache.commons.lang3.SerializationException.java',
        'org.apache.commons.lang3.SerializationUtils.java',
        'org.apache.commons.lang3.StringEscapeUtils.java',
        'org.apache.commons.lang3.StringUtils.java',
        'org.apache.commons.lang3.SystemUtils.java',
        'org.apache.commons.lang3.text.CompositeFormat.java',
        'org.apache.commons.lang3.text.ExtendedMessageFormat.java',
        'org.apache.commons.lang3.text.FormatFactory.java',
        'org.apache.commons.lang3.text.FormattableUtils.java',
        'org.apache.commons.lang3.text.StrBuilder.java',
        'org.apache.commons.lang3.text.StrLookup.java',
        'org.apache.commons.lang3.text.StrMatcher.java',
        'org.apache.commons.lang3.text.StrSubstitutor.java',
        'org.apache.commons.lang3.text.StrTokenizer.java',
        'org.apache.commons.lang3.text.translate.AggregateTranslator.java',
        'org.apache.commons.lang3.text.translate.CharSequenceTranslator.java',
        'org.apache.commons.lang3.text.translate.CodePointTranslator.java',
        'org.apache.commons.lang3.text.translate.EntityArrays.java',
        'org.apache.commons.lang3.text.translate.JavaUnicodeEscaper.java',
        'org.apache.commons.lang3.text.translate.LookupTranslator.java',
        'org.apache.commons.lang3.text.translate.NumericEntityEscaper.java',
        'org.apache.commons.lang3.text.translate.NumericEntityUnescaper.java',
        'org.apache.commons.lang3.text.translate.OctalUnescaper.java',
        'org.apache.commons.lang3.text.translate.UnicodeEscaper.java',
        'org.apache.commons.lang3.text.translate.UnicodeUnescaper.java',
        'org.apache.commons.lang3.text.WordUtils.java',
        'org.apache.commons.lang3.time.DateFormatUtils.java',
        'org.apache.commons.lang3.time.DateParser.java',
        'org.apache.commons.lang3.time.DatePrinter.java',
        'org.apache.commons.lang3.time.DateUtils.java',
        'org.apache.commons.lang3.time.DurationFormatUtils.java',
        'org.apache.commons.lang3.time.FastDateFormat.java',
        'org.apache.commons.lang3.time.FastDateParser.java',
        'org.apache.commons.lang3.time.FastDatePrinter.java',
        'org.apache.commons.lang3.time.FormatCache.java',
        'org.apache.commons.lang3.time.StopWatch.java',
        'org.apache.commons.lang3.tuple.ImmutablePair.java',
        'org.apache.commons.lang3.tuple.ImmutableTriple.java',
        'org.apache.commons.lang3.tuple.MutablePair.java',
        'org.apache.commons.lang3.tuple.MutableTriple.java',
        'org.apache.commons.lang3.tuple.Pair.java',
        'org.apache.commons.lang3.tuple.Triple.java',
        'org.apache.commons.lang3.Validate.java'
        ]

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
    parser = argparse.ArgumentParser(description="Run tasks on Lang project")

    # run buggy of fixed version
    kind_group = parser.add_mutually_exclusive_group(required=True)
    kind_group.add_argument('-f', '--fixed', help='Run fixed versions', action='store_true')
    kind_group.add_argument('-b', '--buggy', help='Run buggy versions', action='store_true')
    # version range
    parser.add_argument('first', type=int, help='first version')
    parser.add_argument('last', type=int, help='last version')
    # commands to run
    parser.add_argument('task', help='task to run', choices=['runDaikon', 'runDaikonOnline', 'split'])
    parser.add_argument('-C', '--chicory_memory', type=int, help='memory size', default=CHICORY_MEM)
    parser.add_argument('-D', '--daikon_memory', type=int, help='memory size', default=DAIKON_MEM)
    parser.add_argument('-T', '--target_memory', type=int, help='memory size', default=TARGET_MEM)
    parser.add_argument('-v', '--queue', help='Cluster queue to use', default=QUEUE)
    parser.add_argument('-n', '--ncpus', type=int, help='cpus to require', default=NCPUS)
    parser.add_argument('-w', '--wall-time', type=int, help='wall time', default=WALL_TIME)
    parser.add_argument('-d', '--dry-run', help="only print commands, won't run it" , action='store_true')
    parser.add_argument('-g', '--debug', help="use debug partation and 30 minutes wall time" , action='store_true')
    parser.add_argument('-l', '--local', help="run locally" , action='store_true')
    parser.add_argument('-s', '--start', type=int, help='start from class #', default=0)
    parser.add_argument('-e', '--end', type=int, help='end at class #', default=len(CLASSES) - 1)


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

    DAIKON = '$PWD/lib/daikon.jar' 
    HAMCREST = '$PWD/lib/hamcrest-core-1.3.jar'
    select_ppt_option = " --ppt-select-pattern={}".format(PACKAGE)

    if args.debug:
        args.wall_time = 30
        args.queue = 'u2-grid-debug'

    if args.start:
        if args.start < 0:
            print 'Start class number must >= 0'
            exit(1)
        elif args.start >= len(CLASSES):
            print 'Start class number must < {}'.format(len(CLASSES))
            exit(1)

    if args.end:
        if args.end < args.start:
            print 'End class number must >= {}'.format(args.start)
            exit(1)
        elif args.end >= len(CLASSES):
            print 'End class number must < {}'.format(len(CLASSES))
            exit(1)

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
        cmd = 'java -d64 -Xmx{}g -cp'.format(args.chicory_memory)
        cmd += ' {}:{}:{}:'.format(DAIKON, JUNIT, HAMCREST)
        cmd += CP
        cmd += ' daikon.Chicory '
        cmd += select_ppt_option  
        cmd += omit_ppt_options
        cmd += SAMPLE
        cmd += COMPARABILITY
        cmd += ' --heap-size={}g'.format(max(args.daikon_memory, args.target_memory))
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

        elif args.task == 'split':
                #do run frontend and daikon on each classe
                for main_ppt in CLASSES[args.start: args.end + 1]:
                    # print(main_ppt)
                    dtraceFile = '{}_{}_{}.dtrace.gz'.format(kind, i, main_ppt)
                    dtraceOutput = ' --dtrace-file=' + dtraceFile
                    select_ppt_option = select_ppt_template.format("^" + main_ppt)
                    txtFile = '{}_{}_s{}_e{}.txt'.format(kind, i, args.start, args.end)
                    invFile = '{}_{}_{}.inv.gz'.format(kind, i, main_ppt)
                    OPTIONS = OPTIONS_TMP.format(invFile)
                    omit_ppts = ''
                    for ppt in CLASSES:
                        if ppt != main_ppt and ppt.find(main_ppt) != -1:
                            omit_ppts += '^{}|'.format(ppt)
                    omit_ppt_options = omit_ppt_template.format(omit_ppts[:-1])

                    cmd = 'java -d64 -Xmx{}g -cp'.format(args.chicory_memory)
                    cmd += ' {}:{}:{}:'.format(DAIKON, JUNIT, HAMCREST)
                    cmd += CP
                    cmd += ' daikon.Chicory '
                    cmd += ' --heap-size={}g'.format(args.target_memory)
                    cmd += select_ppt_option  
                    cmd += omit_ppt_options
                    cmd += SAMPLE
                    cmd += VISIBILITY
                    cmd += COMPARABILITY
                    cmd += dtraceOutput
                    cmd += TEST_CLASS
                    cmds.append(cmd)

                    cmd = 'java -d64 -Xmx{}g -cp'.format(args.daikon_memory)
                    cmd += ' ' + DAIKON
                    cmd += ' daikon.Daikon'
                    cmd += select_ppt_option  
                    cmd += omit_ppt_options
                    cmd += OPTIONS
                    cmd += ' ' + dtraceFile
                    cmds.append(cmd)

                    # cmds.append('''if [ -f {} ]; then\n  rm {}\nfi'''.format(invFile, dtraceFile))
                    cmds.append('rm {}'.format(dtraceFile))

                    cmd = 'java -d64 -Xmx{}g -cp '.format(args.daikon_memory)
                    cmd += DAIKON
                    cmd += ' daikon.PrintInvariants '
                    cmd += invFile
                    cmd += ' >> {}'.format(txtFile)
                    cmds.append(cmd)

                    cmds.append('rm {}'.format(invFile))
        else:
            print "invalid command: " + task
            exit(1)

        generate_script(version, cmds, args.dry_run)
        if args.local:
            execute = './{}.sh'.format(version)
            print(execute)
            if not args.dry_run:
                subprocess.call(execute)
        else:
            submit(version, args.queue, args.ncpus, args.wall_time, args.dry_run)

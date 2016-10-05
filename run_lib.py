import os
import datetime
import time

def run_in_folder(folder, commands, dry_run):
    pwd = os.getcwd()
    if os.path.isdir(folder):
        print '=' * 75
        print '{}: start in folder: {}'.format(datetime.datetime.now() ,folder)
        startTime = time.time()
        os.chdir(folder)
        for cmd in commands:
            print '=' * 40
            print cmd
            if not dry_run:
                jobStarted = time.time()
                print "Command started at: {}".format(datetime.datetime.now())
                os.system(cmd)
                print 'Running time: {} seconds'.format(round(time.time() - jobStarted))
        os.chdir(pwd)
        print '{}: end in folder: {}'.format(datetime.datetime.now() ,folder)
        print 'Total Running time: {} seconds'.format(round(time.time() - startTime))
        print '=' * 75
    else:
        print folder + ' is not a folder!'

def loadRestricts(rFile):
    versions = []
    for line in rFile:
        line = line.lstrip()
        if not line.startswith('#'):
            versions.append(int(line))
    return versions

def loadPPTs(pFile):
    ppts = []
    for line in pFile:
        line = line.lstrip()
        line = line.rstrip('\n\r')
        if not line.startswith('#'):
            lint = line.replace('.', '\.')
            ppts.append(line)
    return ppts

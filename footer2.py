
print("Job started at: {}".format(datetime.datetime.now()))
startTime = time.time()

for cmd in cmds:
    print '='* 75
    print 'Job: {}'.format(cmd)
    jobStarted = time.time()
    subprocess.call('{}'.format(cmd), shell=True)
    print "Running Time: {}".format(round(time.time() - jobStarted))

print("Job ended at: {}".format(datetime.datetime.now()))
print "Total Running Time: {}".format(round(time.time() - startTime))

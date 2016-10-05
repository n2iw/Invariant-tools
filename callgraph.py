def loadGraph(f):
    callerG = {} # caller => list of its called methods
    calledG = {} # called => list of methods that calls it
    for line in f:
        line = line.strip()
        (caller, called, num) = line.split(' ')

        if caller not in callerG:
            callerG[caller] = set()
        callerG[caller].add(called)

        if called not in calledG:
            calledG[called] = set()
        calledG[called].add(caller)

    f.close()
    return callerG, calledG

def loadStaticGraph(f):
    callerG = {} # caller => list of its called methods
    calledG = {} # called => list of methods that calls it
    for line in f:
        line = line.strip()
        if line.startswith('C:'):
            continue
        
        (caller, called) = line.split(' ')
        caller = caller[2:]
        called = called[3:]

        if caller not in callerG:
            callerG[caller] = set()
        callerG[caller].add(called)

        if called not in calledG:
            calledG[called] = set()
        calledG[called].add(caller)

    f.close()
    return callerG, calledG

def loadGraphWithCount(f):
    calledG = {} # called => list of methods that calls it
    calledCount = {}
    for line in f:
        line = line.strip()
        (caller, called, num) = line.split(' ')

        #if caller not in callerG:
            #callerG[caller] = set()
        #callerG[caller].add(called)

        if called not in calledG:
            calledG[called] = set()
            calledCount[called] = 0
        calledG[called].add(caller)
        calledCount[called] += int(num)

    f.close()
    return calledG, calledCount

def loadList(f):
    l = []
    for line in f:
        line = line.strip()
        l.append(line)
    f.close()
    return l

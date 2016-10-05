
print(args)

subprocess.call('hostname', shell=True)
subprocess.call('lscpu | grep "^CPU(s)"', shell=True)
subprocess.call('free -h', shell=True)


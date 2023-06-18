from subprocess import Popen, PIPE
import os
import sys
while 1:
	with open('disp.txt', 'w') as a:
	    sys.stdout = a
	    print(*[line.decode('cp866', 'ignore') for line in Popen('tasklist', stdout=PIPE).stdout.readlines()])
	a.close()
	break

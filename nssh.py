#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from subprocess import Popen, PIPE

import subprocess, shlex
from threading import Timer
	
def run(cmd, timeout_sec=10):
	proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	if timeout_sec <= 0:
		stdout, stderr = proc.communicate()
		exitcode = int(proc.returncode)
	else:
		kill_proc = lambda p: p.kill()
		timer = Timer(timeout_sec, kill_proc, [proc])
		try:
			timer.start()
			stdout, stderr = proc.communicate()
		finally:
			timer.cancel()
	
		exitcode = int(proc.returncode)
	    
		if exitcode == -9 :
			stderr = "Command timed out after {} seconds".format(timeout_sec)
    	
	return (stdout, stderr, exitcode)


testonly=False

if '--test' in sys.argv:
	print ""
	print "--test specified so not going to actually do anything"
	print ""
	testonly=True
	
	
try:
	TIMEOUT=int(os.environ['NSSH_TIMEOUT'])
except:
	TIMEOUT=15	
	
try:
	CMD=sys.argv[1]
except:
	print 'no command specified'
	exit (1)

data = sys.stdin.readlines()




for line in data:
	cmd = 'ssh {} "{}"'.format(line.strip(), CMD)
	if testonly:
		print cmd
	else:
		print line.strip()
		print "___________________________________________________________"
		(out, err, exitcode) = run(cmd, TIMEOUT)
		if exitcode == 0:
			print out
		else:
			print "exit code {}".format(exitcode)
			print err
	
'''
# instead of sshing to one server, ssh to n servers =)

CMD=$1

if [ -z "${CMD+x}" ]; then
	echo "No command specified "
	exit 1	
fi

# read all lines in lines array
while IFS= read -r line; do
	cmd="ssh ${line} \"$CMD\""
	echo $cmd
	$cmd & grep ''
done 


'''

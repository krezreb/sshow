#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from subprocess import Popen, PIPE

import subprocess, shlex
from threading import Timer

def run(cmd, timeout_sec=10):
	proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
	print ("")
	print ("--test specified so not going to actually do anything")
	print ("")
	testonly=True
	
	
try:
	FILE=sys.argv[1]
except:
	print ('no file specified')
	exit (1)

try:
	REMOTE_PATH=sys.argv[2]
except:
	REMOTE_PATH=':'

if REMOTE_PATH[0] != ':':
	REMOTE_PATH = ':'+REMOTE_PATH

TIMEOUT=int(os.getenv('NSCP_TIMEOUT', 15))


data = sys.stdin.readlines()

for line in data:
	cmd = 'scp "{}" {}{}'.format(FILE, line.strip(), REMOTE_PATH)
	if testonly:
		print (cmd)
	else:
		print (line.strip())
		(out, err, exitcode) = run(cmd, TIMEOUT)
		if exitcode == 0:
			print ("OK")
		else:
			print ("exit code {}".format(exitcode))
			print (err)
		
	print ("")
	

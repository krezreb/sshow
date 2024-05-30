#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from subprocess import Popen, PIPE
import argparse

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



parser = argparse.ArgumentParser(description='sshow.', add_help=True)

parser.add_argument('command', default=None, nargs='+', help='command to run remotely')
parser.add_argument('--timeout',default="15", help='Remote command timeout in seconds, can also be set with NSSH_TIMEOUT env var')
parser.add_argument('--sudo', action='store_true', default=False, help='Whether nssh should auto sudo, can also be set via NSSH_SUDO env var')
parser.add_argument('--test', action='store_true', default=False, help="dry run, don't actually run command")


args = parser.parse_args()

if args.test:
	print ("")
	print ("--test specified so not going to actually do anything")
	print ("")
	
try:
	TIMEOUT=int(os.environ['NSSH_TIMEOUT'])
except:
	TIMEOUT=args.timeout	
	
CMD=args.command[0]

if CMD == None:
	print ('No command specified, see nssh -h for help')
	exit (1)

try:
	sudo = os.environ['NSSH_SUDO'][0].lower() in ('y', '1', 'o')
except:
	sudo = args.sudo

if sudo:
	CMD = "sudo {}".format(CMD)

data = sys.stdin.readlines()

for line in data:
	cmd = 'ssh {} "{}"'.format(line.strip(), CMD)
	print (line.strip())
	print ("___________________________________________________________")

	if args.test:
		print (cmd)
		print ("")
	else:
		(out, err, exitcode) = run(cmd, int(TIMEOUT))
		if exitcode == 0:
			if type(out) is bytes:
				out = out.decode('utf-8')
			print (out)
		else:
			print ("exit code {}".format(exitcode))
			print (err)
	

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
from subprocess import Popen, PIPE
import argparse

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
	
parser = argparse.ArgumentParser(description='nscp, multiplexing scp.',
add_help=True,
formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('files', default=None, nargs='*', help='files to upload (or to download if --down set)')
# booleans
parser.add_argument('--up', action='store_true',   help='upload file (default action)')
parser.add_argument('--recursive', '-R', action='store_true', help='Add scp recursive flag')
parser.add_argument('--compress', '-C', action='store_true', help='Add scp compress flag')
parser.add_argument('--down', action='store_true', help='Download rather than upload')
parser.add_argument('--test', action='store_true', help="dry run, don't actually do anything")

args = parser.parse_args()

if args.test:
	print ("")
	print ("--test specified so not going to actually do anything")
	print ("")
	
	
if len(args.files) == 0:
	print ('no files specified')
	exit (1)


TIMEOUT=int(os.getenv('NSCP_TIMEOUT', 15))

data = sys.stdin.readlines()

remote_path='.'
local_path = ""
if args.down:
	if len(args.files) > 2:
		print ("can only download a single path")
		exit(1)
	if len(args.files) == 2:
		local_path = args.files.pop()

else:
	if len(args.files) > 1:
		remote_path = args.files.pop()

scp_args=""
if args.recursive:
	scp_args+=" -R "

if args.compress:
	scp_args+=" -C "

for line in data:
	host =  line.strip()
	# default, upload
	cmd = 'scp {} "{}" {}:{}'.format(scp_args, '" "'.join(args.files), host, remote_path)
		
	if args.down:
		# we're downloading, got to prefix with host to avoid local clobbering
		if not os.path.isdir(host):
			os.makedirs(host)
		local_prefixed_path = "{}/{}".format(host, local_path)
		if local_prefixed_path.endswith("/"):
			local_prefixed_path = local_prefixed_path[0:-1]

		cmd = 'scp {} {}:{} {}'.format(scp_args, host, args.files[0], local_prefixed_path)
	
	if args.test:
		print (cmd)
		continue

	print (line.strip())
	(out, err, exitcode) = run(cmd, TIMEOUT)
	if exitcode == 0:
		print ("OK")
	else:
		print ("exit code {}".format(exitcode))
		print (err)
		
	print ("")
	

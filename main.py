#!/usr/bin/python
# -*- coding: utf-8 -*-

from wifiBox import client_wifi, wifiBox
from utils import global_listening, monitoring
from parseXML import parsing_global, prepare_wep_listining
from ListeningManager import ListeningManager
from time import sleep
import os
import signal

if __name__ == '__main__':
    print "QQ"
    print "Mise en place du monitoring"
    monitoring()
    # On effectue une écoute globale
    print "Début de l'écoute globale"
    dir_path = "TestBox/global"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    global_pid = global_listening()
    lm_wep = ListeningManager()
    cpt = 0
    while cpt != 12 * 60:
        sleep(5)
        parsing_global()
        wep_list = prepare_wep_listining()
        lm_wep.updateNetworkTable(wep_list)
        lm_wep.display()
        lm_wep.updateListening()
        cpt = cpt + 1
    os.killpg(global_pid, signal.SIGTERM)
    lm_wep.destroy()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from wifiBox import client_wifi, wifiBox
from utils import global_listening, monitoring
from parseXML import parsing_global, prepare_wep_listining
from ListeningManager import ListeningManager
import time
import os
import signal, sys
import logging

import sys, signal, time

lm_wep = ListeningManager(10)
global_pid = -1
stand_still = True

signals = [signal.SIGTERM
        , signal.SIGINT
        , signal.SIGHUP
        , signal.SIGQUIT]

def handler(signum = None, frame = None):
    global stand_still
    stand_still = False
    logging.warning('Signal handler called with signal')

if __name__ == '__main__':
    logging.basicConfig(filename='wifisecure.log', level=logging.INFO, format='[%(levelname)s|%(asctime)s]: %(message)s', datefmt='%m/%d %I:%M:%S')
    for sig in signals:
        signal.signal(sig, handler)

    logging.info("Starting monitoring...")
    found_wlan = monitoring()
    if(found_wlan):
        logging.info("Stating global_listening..")
        dir_path = "TestBox/global"
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        global_pid = global_listening()
        while stand_still:
            time.sleep(2)
            parsing_global()
            wep_list = prepare_wep_listining()
            lm_wep.updateNetworkTable(wep_list)
            lm_wep.updateListening()
            lm_wep.display()

        lm_wep.destroy()
        os.killpg(global_pid, signal.SIGTERM)
    else:
        logging.critical("Can't start the process. Please connext a rt2800 card")
    logging.info("End of the program")

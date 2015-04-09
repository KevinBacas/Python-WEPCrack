#!/usr/bin/python
# -*- coding: utf-8 -*-

from Utils import network_listening, arp_attack, keep_alive_packet, result_aircrack_wep, result_aircrack_wpa
from WEPListening import WEPListening
from WPAListening import WPAListening
import threading
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

        # for network in self.listeningList:
        #     if network.box not in tmpTable:
        #         index = self.listeningList.index(network)
        #         self.listeningList.pop(index)
        #         network.stopListening()

        for qq in self.listeningList:
            qq.update()

    def destroy(self):
        """
        Destroy all the listening threads (Safe exit)
        """
        for listen in self.listeningList:
            listen.stopListening()

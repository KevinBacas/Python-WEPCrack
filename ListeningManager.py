#!/usr/bin/python
# -*- coding: utf-8 -*-

from utils import network_listening, arp_attack
import os
import signal

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

    def stopListening(self):
        print "Stoping... %s" % (self.box)
        os.killpg(self.focus_listen_pid, signal.SIGTERM)
        os.killpg(self.arp_pid, signal.SIGTERM)

    def __eq__(self, other):
        return self.box == other.box

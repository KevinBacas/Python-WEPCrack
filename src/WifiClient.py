#!/usr/bin/python
# -*- coding: utf-8 -*-

class WifiClient:
    """
    Wifi client is a class to capture important information of a client
    A client is someone who is connected to a box
    """
    def __init__(self, MAC_CLIENT):
        """
        :param MAC_CLIENT: client's mac adress
        """
        self._MAC_CLIENT = MAC_CLIENT

    def display(self):
        """
        display client's information
        """
        print self._MAC_CLIENT

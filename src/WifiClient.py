#!/usr/bin/python
# -*- coding: utf-8 -*-

class WifiClient:
    """
    Classe capturant les informations utiles lors d'une écoute local
    """
    def __init__(self, MAC_CLIENT):
        self._MAC_CLIENT = MAC_CLIENT

    def display(self):
        print self._MAC_CLIENT

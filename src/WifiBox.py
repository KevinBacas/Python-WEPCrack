#!/usr/bin/python
# -*- coding: utf-8 -*-

class WifiBox:
    """
    Classe capturant les informations utiles lors d'une écoute globale.
    """
    def __init__(self, BSSID, ESSID, Encryption, Data, Channel, PWR):
        self._BSSID = BSSID
        self._ESSID = ESSID
        self._Encryption = Encryption
        self._Data = Data
        self._Channel = Channel
        self._PWR = PWR


    def __str__(self):
    	"""
    	Affiche le contenu d'une box
    	"""
        res = "{ ESSID : %s , data : %d }" % (self._ESSID, self._Data)
        return res


    def superior(self, wifiBox):
    	"""
    	Obsolete
    	"""
        if abs(self._Data) > abs(wifiBox._Data):
            return self
        elif abs(self._PWR)  > abs(wifiBox._PWR) :
            return self
        else:
            return wifiBox

    def __eq__(self, other):
        return self._ESSID == other._ESSID

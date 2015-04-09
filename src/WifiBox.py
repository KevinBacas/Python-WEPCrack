#!/usr/bin/python
# -*- coding: utf-8 -*-

class WifiBox:
    """
    Classe capturant les informations utiles lors d'une écoute globale.
    """
    def __init__(self, BSSID, ESSID, Encryption, Data, Channel, PWR):
        """
        :param BSSID: BSSID of the box
        :param ESSID: ESSID of the box
        :param Encryption: Encryption the box uses (WPA/WPA2 or WEP)
        :param Data: amount of data you see from the box
        :param Channel: Channel the box is in
        :param PWR: the signal power you get from the box
        """
        self._BSSID = BSSID
        self._ESSID = ESSID
        self._Encryption = Encryption
        self._Data = Data
        self._Channel = Channel
        self._PWR = PWR


    def __str__(self):
        """
        display the name (ESSID) and the data of the box
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

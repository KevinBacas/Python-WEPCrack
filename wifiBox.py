class wifiBox:
    def __init__(self, BSSID, ESSID, Encryption, Data, Channel, PWR):
        self._BSSID = BSSID
        self._ESSID = ESSID
        self._Encryption = Encryption
        self._Data = Data
        self._Channel = Channel
        self._PWR = PWR

    def display(self):
        print self._BSSID
        print self._ESSID
        print self._Encryption
        print "data :" + str(self._Data)
        print "chan :" + str(self._Channel )
        print "pwr :" + str(self._PWR )

    def superior(self, wifiBox):
        if abs(self._Data) > abs(wifiBox._Data):
            return self
        elif abs(self._PWR)  > abs(wifiBox._PWR) :
            return self
        else:
            return wifiBox

def abs( nombre ):
    if nombre < 0:
        return -1*nombre
    else:
        return nombre


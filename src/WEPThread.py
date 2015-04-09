#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import threading
import time
import re
import logging
import signal
from Utils import aircrack_final_wep, get_key


class WEPThread(threading.Thread):
    """
    WEPThread is specific class to handle the threads generate to crack the key while
    the WEP network is being attacked
    """
    def __init__(self, box, datafile_path, name='WEP_thread'):
        """
        :param box: The box to crack
        :param datafile_path: The path to the box directory
        :param name: The name you give to the tread
        """
        self.pro = None
        self._continue = True
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name=name)
        self.box = box
        self.path = datafile_path

    def run(self) :
        """
        The method which is launch when the thread is started
        """
        key_file_name = self.box._ESSID + ".result"
        KEY = ""
        self.pro = aircrack_final_wep(self.path)
        while KEY == "" and self._continue == True :
            if self.pro.poll() != None:
                logging.warning("%s n'a pas reussi à lancer Aircrack-ng", self.path)
                self.pro = aircrack_final_wep(self.path)
            KEY = get_key(key_file_name)
            time.sleep(5)
        if KEY != "":
            cmd = "echo \" WEP_box_path : " + self.box._ESSID + " with key " + KEY + "\" >> key.result"
            FNULL = open(os.devnull, 'w')
            subprocess.Popen(cmd, stdout=FNULL, shell=True, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        os.killpg(self.pro.pid, signal.SIGKILL)

    def stop(self, timeout=None):
        """
        stop the thread
        :param timeout: optional, time you let to the thread before stopping it
        """
        self._continue = False

    def join(self, timeout=None):
        """
        join the thread
        :param timeout: optional, time you let to the thread before stopping it
        """
        self._stopevent.set()
        threading.Thread.join(self, timeout)

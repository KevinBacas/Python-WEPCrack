#!/usr/bin/python
# -*- coding: utf-8 -*-

from Utils import network_listening, result_aircrack_wpa
import threading
import signal
import logging
import os
from WPAThread import WPAThread

class WPAListening():
    """
    WPAListening is a specific class to handle the cracking of a Wifibox
    which uses WPA security

    .. todo: Create a SuperClass to merge WEPListening and WPAListening common behaviours
    """
    def __init__(self, box):
        """
        :param box: The box to crack

        .. note:: It creates also 2 fields to handle the pids of processing threads
        """
        self.box = box
        self.focus_listen_pid = None
        self.aircrack_thread = None

    def startListening(self):
	"""
        start the listening and exectue all the processes to attack a network
	"""
        logging.info("Starting listening on %s", self.box._ESSID)
        dir_path = "TestBox/" + self.box._ESSID
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        self.focus_listen_pid = network_listening(self.box)
        self.aircrack_thread = WPAThread(self.box, dir_path)
        self.aircrack_thread.start()

    def update(self):
        pass

    def stopListening(self):
	"""
        close all the processes and stop the listening
	"""
        logging.info("Stopping listening on %s...", self.box._ESSID)
        try:
            os.killpg(self.focus_listen_pid, signal.SIGTERM)
        except:
            pass
        self.aircrack_thread.stop()
        logging.info("Listening on %s stopped !", self.box._ESSID)

    def __eq__(self, other):
	"""
	Check if two box are equal
	:param box: the box you're comparing with
	"""
        return self.box == other.box
